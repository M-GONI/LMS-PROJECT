class MemberCollection:
    """Manages all members."""

    def __init__(self):
        self._members = {}  # dictionary

    def add_member(self, member):
        if member.get_member_id() in self._members:
            raise ValueError("Member already exists")
        self._members[member.get_member_id()] = member

    def remove_member(self, member_id):
        if member_id not in self._members:
            raise KeyError("Member not found")
        del self._members[member_id]

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