"""
Audit outputs helper command
"""
import collections
import datetime as dt
import json
import sys

from django.core.management.base import BaseCommand
import reversion

from opal.models import Tagging
from elcid.tags import TAGS

deleted_tags = reversion.get_deleted(Tagging)
DELETED_TAG_DATA = [json.loads(d.serialized_data)[0]['fields'] for d in deleted_tags]

class MonthlyAudit(object):
    def __init__(self, tag_name):
        self.tag_name = tag_name
        self.episodes = []
        self.ages = collections.defaultdict(int)
        self.diagnoses = collections.defaultdict(int)
        self.length_of_stay = collections.defaultdict(int)

    @property
    def num_patients(self):
        return len(self.episodes)

    def get_episodes(self):
        """
        1. Get all episodes currently tagged with self.TAG_NAME
        2. Get all historically tagged episodes for self.TAG_NAME
        3. Append both to self.EPISODES
        """
        current = [t.episode for t in
                   Tagging.objects.filter(tag_name=self.tag_name)]
        our_deleted = [t for t in DELETED_TAG_DATA if t['tag_name'] == self.tag_name]
        historic = [Episode.objects.get(pk=t['episode']) for t in our_deleted]
        current += historic
        self.episodes = list(set(current))
        return

    def calculate_stats(self):
        self.get_episodes()
        for episode in self.episodes:
            patient = episode.patient
            demographics = patient.demographics_set.get()
            diagnoses = episode.diagnosis_set.all()

            # Log age distribution
            if demographics.date_of_birth:
                age = (dt.date.today() - demographics.date_of_birth).days / 365
                self.ages[age] += 1

            # Log diagnoses
            for d in diagnoses:
                self.diagnoses[d.condition] += 1

            if episode.discharge_date:
                days = (episode.discharge_date - episode.date_of_admission).days
                self.length_of_stay[days] += 1

        return

    def print_stats(self):
        print self.tag_name
        print self.num_patients
        print self.ages
        print self.diagnoses
        print self.length_of_stay
        return

    def to_dict(self):
        return dict(
                tag_name=self.tag_name,
                num_patients=self.num_patients,
                ages=self.ages,
                diagnoses=self.diagnoses,
                length_of_stay=self.length_of_stay
                )


def get_all_tag_names():
    tag_names = []
    for internal, _, subtags in TAGS:
        tag_names.append(internal)
        if subtags:
            for internal, _, _ in subtags:
                tag_names.append(internal)
    tag_names.remove('mine')
    return tag_names


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        """
        1. List all current and historic tag names in a datastructure
        2. Calculate summary statistics for all tag names.
        """
        tag_names = get_all_tag_names()
        out = []
        for tag in tag_names:
            report = MonthlyAudit(tag)
            report.calculate_stats()
            out.append(report.to_dict())
        print json.dumps(out, indent=2)
