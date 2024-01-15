from typing import Optional, List, Dict
from linkedin_api import Linkedin
import re
import os
from dotenv import load_dotenv
from collections import defaultdict

load_dotenv()


class Profile:
    def __init__(self, linkedin_url):
        self.linkedin_url = linkedin_url
        self.basic_info: defaultdict = defaultdict()
        self.works_info: List[defaultdict] = []
        self.volunteers_info: List[defaultdict] = []
        self.project_info: List[defaultdict] = []
        self.edu_info: List[defaultdict] = []
        self.certificates_info: List[defaultdict] = []
        self.awards_info: List[defaultdict] = []
        self.publications_info: List[defaultdict] = []
        self.skills_info: List[str] = []
        self.language_info: List[defaultdict] = []
        self.reference_info: List[defaultdict] = []

    def get_id(self):
        return re.findall(r"linkedin.com/in/(.*)/", self.linkedin_url)[0]

    @classmethod
    def from_text_files(txt_file) -> List["Profile"]:
        raise NotImplementedError

    def _build_profile_basic(self, _candidate: dict):
        try:
            self.basic_info["name"] = (
                _candidate["firstName"] + " " + _candidate["lastName"]
            )
            self.basic_info["headline"] = _candidate["headline"]
            self.basic_info["summary"] = _candidate["summary"]
            self.basic_info["location"] = _candidate["locationName"]
            self.basic_info["linkedin"] = _candidate["linkedin"]
        except KeyError as e:
            print("Error: Missing key in candidate data -", e)
            print("Partial data will be saved.")
        except Exception as e:
            print("Error: An unexpected error occurred -", e)
            print("Partial data will be saved")

    def _build_profile_works(self, _candidate: dict):
        for exp in _candidate["experience"]:
            try:
                work = defaultdict()
                work["company"] = exp["companyName"]
                work["position"] = exp["title"]
                work["summary"] = exp["description"]
                work["startdate"] = (
                    str(exp["timePeriod"]["startDate"]["year"])
                    + "-"
                    + str(exp["timePeriod"]["startDate"]["month"])
                )
                if exp["timePeriod"].get("endDate") == None:
                    work["enddate"] = ""
                else:
                    work["enddate"] = (
                        str(exp["timePeriod"]["endDate"]["year"])
                        + "-"
                        + str(exp["timePeriod"]["endDate"]["month"])
                    )
                self.works_info.append(work)
            except KeyError as e:
                print("Error: Missing key in candidate data -", e)
                print("Partial data will be saved.")
                self.works_info.append(work)
            except Exception as e:
                print("Error: An unexpected error occurred -", e)
                print("Partial data will be saved")
                self.works_info.append(work)

    def _build_profile_volunteers(self, _candidate: dict):
        for exp in _candidate["volunteer"]:
            volunteer = defaultdict()

            try:
                # TODO fill this
                raise NotImplementedError

            except KeyError as e:
                print("Error: Missing key in candidate data -", e)
                print("Partial data will be saved.")
                self.volunteers_info.append(volunteer)

            except Exception as e:
                print("Error: An unexpected error occurred -", e)
                print("Partial data will be saved")
                self.volunteers_info.append(volunteer)

    def _build_profile_projects(self, _candidate: dict):
        for exp in _candidate["experience"]:
            project = defaultdict()

            try:
                # TODO fill this
                raise NotImplementedError

            except KeyError as e:
                print("Error: Missing key in candidate data -", e)
                print("Partial data will be saved.")
                self.project_info.append(project)

            except Exception as e:
                print("Error: An unexpected error occurred -", e)
                print("Partial data will be saved")
                self.project_info.append(project)

    def _build_profile_edus(self, _candidate: dict):
        for edu in _candidate["education"]:
            edu = defaultdict()

            try:
                # TODO fill this
                raise NotImplementedError

            except KeyError as e:
                print("Error: Missing key in candidate data -", e)
                print("Partial data will be saved.")
                self.edu_info.append(edu)

            except Exception as e:
                print("Error: An unexpected error occurred -", e)
                print("Partial data will be saved")
                self.edu_info.append(edu)

    def _build_profile_certificates(self, _candidate: dict):
        for cert in _candidate["certification"]:
            cert = defaultdict()

            try:
                # TODO fill this
                raise NotImplementedError

            except KeyError as e:
                print("Error: Missing key in candidate data -", e)
                print("Partial data will be saved.")
                self.certificates_info.append(cert)

            except Exception as e:
                print("Error: An unexpected error occurred -", e)
                print("Partial data will be saved")
                self.certificates_info.append(cert)

    def _build_profile_awards(self, _candidate: dict):
        for award in _candidate["award"]:
            award = defaultdict()

            try:
                # TODO fill this
                raise NotImplementedError

            except KeyError as e:
                print("Error: Missing key in candidate data -", e)
                print("Partial data will be saved.")
                self.awards_info.append(award)

            except Exception as e:
                print("Error: An unexpected error occurred -", e)
                print("Partial data will be saved")
                self.awards_info.append(award)

    def _build_profile_publications(self, _candidate: dict):
        for pub in _candidate["publication"]:
            pub = defaultdict()

            try:
                # TODO fill this
                raise NotImplementedError

            except KeyError as e:
                print("Error: Missing key in candidate data -", e)
                print("Partial data will be saved.")
                self.publications_info.append(pub)

            except Exception as e:
                print("Error: An unexpected error occurred -", e)
                print("Partial data will be saved")
                self.publications_info.append(pub)

    def _build_profile_skills(self, _candidate: dict):
        for skill in _candidate["skill"]:
            try:
                self.skills_info.append(skill["name"])
            except KeyError as e:
                print("Error: Missing key in candidate data -", e)
                print("Partial data will be saved.")
                self.skills_info.append(skill["name"])
            except Exception as e:
                print("Error: An unexpected error occurred -", e)
                print("Partial data will be saved")
                self.skills_info.append(skill["name"])

    def _build_profile_languages(self, _candidate: dict):
        for lang in _candidate["language"]:
            lang = defaultdict()

            try:
                # TODO fill this
                raise NotImplementedError

            except KeyError as e:
                print("Error: Missing key in candidate data -", e)
                print("Partial data will be saved.")
                self.language_info.append(lang)

            except Exception as e:
                print("Error: An unexpected error occurred -", e)
                print("Partial data will be saved")
                self.language_info.append(lang)

    def _build_profile_references(self, _candidate: dict):
        for ref in _candidate["reference"]:
            ref = defaultdict()

            try:
                # TODO fill this
                raise NotImplementedError

            except KeyError as e:
                print("Error: Missing key in candidate data -", e)
                print("Partial data will be saved.")
                self.reference_info.append(ref)

            except Exception as e:
                print("Error: An unexpected error occurred -", e)
                print("Partial data will be saved")
                self.reference_info.append(ref)


if __name__ == "__main__":
    raise NotImplementedError
