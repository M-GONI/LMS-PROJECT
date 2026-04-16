import json
import os
from src.models.member import Member


class MemberCollection:
    """Manages all members."""

    def __init__(self, json_file="members_data.json"):
        self._members = {}  # dictionary
        self.json_file = json_file
        self.load_from_json()

    def add_member(self, member):
        if member.get_member_id() in self._members:
            raise ValueError("Member already exists")
        self._members[member.get_member_id()] = member
        self.save_to_json()

    def remove_member(self, member_id):
        if member_id not in self._members:
            raise KeyError("Member not found")
        del self._members[member_id]
        self.save_to_json()

    def find_by_id(self, member_id):
        return self._members.get(member_id)

    def find_by_name(self, name):
        result = []
        for member in self._members.values():
            if name.lower() in member.get_name().lower():
                result.append(member)
        return result

    def count(self):
        return len(self._members)

    def get_all_members(self):
        return list(self._members.values())

    def save_to_json(self):
        """Save all members to a JSON file."""
        data = []
        for member in self._members.values():
            data.append({
                "name": member.get_name(),
                "member_id": member.get_member_id(),
                "email": member.get_email(),
                "borrowed_books": member.get_borrowed_books(),
                "fines_owed": member.get_fines()
            })
        with open(self.json_file, 'w') as f:
            json.dump(data, f, indent=4)

    def load_from_json(self):
        """Load all members from a JSON file."""
        if not os.path.exists(self.json_file):
            return  # File doesn't exist yet, start fresh
        
        try:
            with open(self.json_file, 'r') as f:
                data = json.load(f)
            
            self._members = {}
            for item in data:
                member = Member(item["name"], item["member_id"], item["email"])
                # Restore other attributes if they exist
                if "borrowed_books" in item:
                    member._borrowed_books = item["borrowed_books"]
                if "fines_owed" in item:
                    member._fines_owed = item["fines_owed"]
                self._members[member.get_member_id()] = member
        except (json.JSONDecodeError, KeyError, TypeError):
            # If there's an error reading the file, start fresh
            self._members = {}