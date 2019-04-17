from datetime import datetime

from app.models import Version


class InMemoryDatastore:
    def __init__(self):
        self.data = {
            "mbs": {
                "eq_id": "mbs",
                "form_type": "0001",
                "created_by": "Samiwel Thomas",
                "created_at": str(datetime.utcnow()),
                "versions": [
                    Version(
                        "1", "0001", {"hello": "world"}, "a Thomas", "en", None, None
                    ),
                    Version("2", "0001", {}, "b Thomas", "en", None, None),
                    Version("3", "0001", {}, "c Thomas", "en", None, None),
                    Version("4", "0001", {}, "d Thomas", "en", None, None),
                ],
            },
            "qpses": {
                "eq_id": "qpses",
                "form_type": "0169",
                "created_by": "Samiwel Thomas",
                "created_at": str(datetime.utcnow()),
                "versions": [
                    Version("1", "0169", {}, "a Thomas", "en", None, None),
                    Version("2", "0169", {}, "b Thomas", "en", None, None),
                    Version("3", "0169", {}, "c Thomas", "en", None, None),
                    Version("4", "0169", {}, "d Thomas", "en", None, None),
                ],
            },
        }

    def get_latest_versions(self):
        latest_versions = []

        for k, v in self.data.items():
            latest = next(iter(v.get("versions")), None)
            if latest:
                latest_versions.append({"name": k, "version": latest.to_json()})

        return latest_versions

    def get_questionnaire_by_name(self, questionnaire_name):
        return self.data.get(questionnaire_name)

    def create_questionnaire(self, questionnaire_name, form_type, created_by):
        self.data[questionnaire_name] = {
            "eq_id": questionnaire_name,
            "form_type": form_type,
            "created_by": created_by,
            "created_at": str(datetime.utcnow()),
            "versions": [],
        }

    def create_version(self, questionnaire_name, version):
        self.data[questionnaire_name].get("versions").append(version)

    def get_version(self, questionnaire_name, version_id):

        version = next(
            iter(
                filter(
                    lambda v: v.id == version_id,
                    self.data[questionnaire_name].get("versions"),
                )
            ),
            None,
        )

        return version.data if version else None
