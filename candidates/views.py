import json
import re

from slumber.exceptions import HttpClientError
from popit_api import PopIt
from slugify import slugify
import requests
from urlparse import urlunsplit

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render
from django.utils.http import urlquote
from django.views.generic import FormView, TemplateView, DeleteView

from .forms import PostcodeForm, CandidacyForm
from .models import PopItPerson


class PopItApiMixin(object):

    def __init__(self, *args, **kwargs):
        super(PopItApiMixin, self).__init__(*args, **kwargs)
        self.api = PopIt(
            instance=settings.POPIT_INSTANCE,
            hostname=settings.POPIT_HOSTNAME,
            port=settings.POPIT_PORT,
            api_version='v0.1',
            user=settings.POPIT_USER,
            password=settings.POPIT_PASSWORD,
            append_slash=False,
        )

    def get_search_url(self, collection, query):
        port = settings.POPIT_PORT
        instance_hostname = settings.POPIT_INSTANCE + \
            '.' + settings.POPIT_HOSTNAME
        if port != 80:
            instance_hostname += ':' + str(port)
        base_search_url = urlunsplit(
            ('http', instance_hostname, '/api/v0.1/search/', '', '')
        )
        return base_search_url + collection + '?q=' + urlquote(query)


def get_candidate_list_popit_id(constituency_name, year):
    """Return the PopIt organization ID for a constituency's candidate list

    >>> get_candidate_list_popit_id('Leeds North East', 2010)
    'candidates-2010-leeds-north-east'
    >>> get_candidate_list_popit_id('Ayr, Carrick and Cumnock', 2015)
    'candidates-2015-ayr-carrick-and-cumnock'
    """
    return 'candidates-{year}-{slugified_name}'.format(
        year=year,
        slugified_name=slugify(constituency_name),
    )


class ConstituencyFinderView(FormView):
    template_name = 'candidates/finder.html'
    form_class = PostcodeForm

    def form_valid(self, form):
        postcode = form.cleaned_data['postcode']
        url = 'http://mapit.mysociety.org/postcode/' + postcode
        r = requests.get(url)
        if r.status_code == 200:
            mapit_result = r.json
            mapit_constituency_id = mapit_result['shortcuts']['WMC']
            mapit_constituency_data = mapit_result['areas'][str(mapit_constituency_id)]
            constituency_url = reverse(
                'constituency',
                kwargs={'constituency_name': mapit_constituency_data['name']}
            )
            return HttpResponseRedirect(constituency_url)
        else:
            error_url = reverse('finder')
            error_url += '?bad_postcode=' + urlquote(postcode)
            return HttpResponseRedirect(error_url)

    def get_context_data(self, **kwargs):
        context = super(ConstituencyFinderView, self).get_context_data(**kwargs)
        bad_postcode = self.request.GET.get('bad_postcode')
        if bad_postcode:
            context['bad_postcode'] = bad_postcode
        return context


def get_members(api, organization_id):
    candidate_data = api.organizations(organization_id).get()['result']
    return [ m['person_id'] for m in candidate_data['memberships'] ]

def membership_exists(api, person_id, organization_id):
    return person_id in get_members(api, organization_id)

def delete_membership(api, person_id, organization_id):
    candidate_data = api.organizations(organization_id).get()['result']
    for m in candidate_data['memberships']:
        if m['person_id'] == person_id:
            api.memberships(m['id']).delete()


class ConstituencyDetailView(PopItApiMixin, TemplateView):
    template_name = 'candidates/constituency.html'

    def get_context_data(self, **kwargs):
        context = super(ConstituencyDetailView, self).get_context_data(**kwargs)

        constituency_name = kwargs['constituency_name']

        old_candidate_list_id = get_candidate_list_popit_id(constituency_name, 2010)
        new_candidate_list_id = get_candidate_list_popit_id(constituency_name, 2015)

        old_candidate_ids = get_members(self.api, old_candidate_list_id)
        new_candidate_ids = get_members(self.api, new_candidate_list_id)

        person_id_to_person_data = {
            person_id: PopItPerson.create_from_popit(self.api, person_id)
            for person_id in set(old_candidate_ids + new_candidate_ids)
        }

        context['new_candidate_list_id'] = new_candidate_list_id

        context['candidates_2010'] = [
            (person_id_to_person_data[p_id], p_id in new_candidate_ids)
            for p_id in old_candidate_ids
        ]
        context['candidates_2015'] = [
            person_id_to_person_data[p_id] for p_id in new_candidate_ids
        ]
        context['constituency_name'] = constituency_name

        return context


class CandidacyMixin(object):

    def get_person_and_organization(self, form):
        # If either of these don't exist, an HttpClientError will be
        # thrown, which is fine for error checking at the moment
        organization_id = form.cleaned_data['organization_id']
        person_id = form.cleaned_data['person_id']
        try:
            organization_data = self.api.organizations(organization_id).get()['result']
            person_data = self.api.persons(person_id).get()['result']
        except HttpClientError as e:
            if e.response.status_code == 404:
                return HttpResponseBadRequest('Unknown organization_id or person_id')
            else:
                raise
        return (person_data, organization_data)

    def redirect_to_constituency(self, candidate_list_data):
        m = re.search(
            r'^Candidates for (.*) in \d+$',
            candidate_list_data['name']
        )
        if m:
            constituency_name = m.group(1)
            return HttpResponseRedirect(
                reverse('constituency',
                        kwargs={'constituency_name': constituency_name})
            )
        else:
            message = "Failed to parse the candidate_list_name '{0}'"
            raise Exception(message.format(candidate_list_name))


class CandidacyView(PopItApiMixin, CandidacyMixin, FormView):

    form_class = CandidacyForm

    def form_valid(self, form):
        person_data, organization_data = self.get_person_and_organization(form)
        print json.dumps(person_data, indent=4)
        person_id = person_data['id']
        candidate_list_id = organization_data['id']
        # Check that that membership doesn't already exist:
        if not membership_exists(self.api, person_id, candidate_list_id):
            # Try to create the new membership
            self.api.memberships.post({
                'organization_id': candidate_list_id,
                'person_id': person_id,
            })
        return self.redirect_to_constituency(organization_data)


class CandidacyDeleteView(PopItApiMixin, CandidacyMixin, FormView):

    form_class = CandidacyForm

    def form_valid(self, form):
        person_data, organization_data = self.get_person_and_organization(form)
        person_id = person_data['id']
        candidate_list_id = organization_data['id']
        delete_membership(self.api, person_id, candidate_list_id)
        return self.redirect_to_constituency(organization_data)
