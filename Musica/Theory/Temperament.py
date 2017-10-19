####################################################################################################
#
# Musica - A Music Theory Package for Python
# Copyright (C) 2017 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
####################################################################################################

"""This module defines temperaments.

"""

####################################################################################################

__all__ = [
    'EqualTemperament',
    'ET12',
    ]

####################################################################################################

from ..Locale.Note import translate_et12_note
from .PitchStandard import A440

####################################################################################################

class EqualTemperament:

    """Class to define an Equal Temperament.

    Step is an alias for semitone.
    """

    ##############################################

    def __init__(self, number_of_steps, pitch_standard):

        self._number_of_steps = number_of_steps
        self._pitch_standard = pitch_standard

        self._fundamental = self._compute_fundamental()

    ##############################################

    @property
    def number_of_steps(self):
        return self._number_of_steps

    @property
    def pitch_standard(self):
        return self._pitch_standard

    @property
    def fundamental(self):
        """Return the frequency of C0"""
        return self._fundamental

    ##############################################

    def _compute_scale(self, octave, step_number):

        octave_factor = 2 ** octave
        interval_factor = 2 ** (step_number / self._number_of_steps)
        return octave_factor * interval_factor

    ##############################################

    def _compute_fundamental(self):

        denominator = self._compute_scale(self._pitch_standard.octave,
                                          self._pitch_standard.step_number)
        return self._pitch_standard.frequency / denominator

    ##############################################

    def frequency(self, octave, step_number):

        """Return the frequency for an octave using the scientific pitch notation and an step number
        ranging from 0 to 11.

        For A440 (La3), use octave 4 and step number 9.

        """

        return self._fundamental * self._compute_scale(octave, step_number)

####################################################################################################

class UsualEqualTemperament(EqualTemperament):

    """Base class factory to build for example a twelve-tone equal temperament.
    """

    ##############################################

    def __init__(self, number_of_steps, pitch_standard, step_name_to_number, translator):

        super().__init__(number_of_steps, pitch_standard)

        self._translator = translator

        # Map   note name -> number of semitones
        self._step_name_to_number = step_name_to_number

        # Note name
        #   ensure name are sorted by degree
        self._step_names = sorted(step_name_to_number.keys(), key=lambda x: step_name_to_number[x])

        # Map   number of semitones -> note name
        #   accidental steps are set to None
        self._step_number_to_name = [None]*number_of_steps
        for name, step_number in step_name_to_number.items():
            self._step_number_to_name[step_number] = name
        #   add accidentals
        for i in range(number_of_steps):
            if self._step_number_to_name[i] is None:
                if i > 0:
                    self._step_name_to_number[self._step_number_to_name[i-1] + '#'] = i
                if i < 11:
                    self._step_name_to_number[self._step_number_to_name[i+1] + '-'] = i

    ##############################################

    @property
    def step_names(self):
        return self._step_names

    @property
    def number_of_names(self):
        return len(self._step_names)

    ##############################################

    def translator(self, *args, **kwargs):
        return self._translator(*args, **kwargs)

    ##############################################

    def is_valid_step_name(self, name):
        return name in self._step_names

    ##############################################

    def is_valid_step_number(self, number):
        return 0 < number < self._number_of_steps

    ##############################################

    def name_to_number(self, name):
        return self._step_name_to_number[name]

    ##############################################

    def number_to_name(self, name):
        return self._step_number_to_name[name]

    ##############################################

    def degree_to_name(self, degree):
        return self._step_names[degree]

    ##############################################

    def name_to_degree(self, name):

        if name in self._step_names:
            return self._step_names.index(name)
        else:
            raise ValueError("Invalid name {}".format(name))

####################################################################################################

#: Twelve-tone equal temperament, also known as 12 equal temperament, 12-TET, or 12-ET
ET12 = UsualEqualTemperament(
    number_of_steps=12,
    pitch_standard=A440,
    step_name_to_number={
        'C' : 0,
        'D' : 2,
        'E' : 4,
        'F' : 5,
        'G' : 7,
        'A' : 9,
        'B' : 11,
    },
    translator=translate_et12_note,
)