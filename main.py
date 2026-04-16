from models.member import Member
from models.member_collection import MemberCollection


def main():
    collection = MemberCollection()

    while True:
        print("\n==== Library Member System ====")
        print("1. Add Member")
        print("2. View All Members")
        print("3. Find Member by ID")
        print("4. Remove Member")
        print("5. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            name = input("Enter name: ")
            member_id = input("Enter ID: ")
            email = input("Enter email: ")

            member = Member(name, member_id, email)
            try:
                collection.add_member(member)
                print("✅ Member added successfully")
            except ValueError as e:
                print("❌", e)

        elif choice == "2":
            members = collection.get_all_members()
            if not members:
                print("No members found")
            else:
                for m in members:
                    print(f"{m.get_member_id()} - {m.get_name()}")

        elif choice == "3":
            member_id = input("Enter ID: ")
            member = collection.find_by_id(member_id)
            if member:
                print(f"Found: {member.get_name()} ({member.get_member_id()})")
            else:
                print("Member not found")

        elif choice == "4":
            member_id = input("Enter ID to remove: ")
            try:
                collection.remove_member(member_id)
                print("✅ Member removed")
            except KeyError as e:
                print("❌", e)

        elif choice == "5":
            print("Exiting...")
            break

        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()