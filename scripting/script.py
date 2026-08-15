# ADD CODE HERE
# change script to whatever language you are comfortable with


import json
import sys


def get_changed_attributes(before, after):
    """
    Return the top-level attributes that changed between
    the before and after resource states.
    """

    before = before or {}
    after = after or {}

    changed = set()

    all_keys = set(before.keys()) | set(after.keys())

    for key in all_keys:
        if before.get(key) != after.get(key):
            changed.add(key)

    return changed


def only_git_commit_hash_changed(before, after):
    """
    An update is allowed only when:
      1. The only top-level attribute changed is 'tags'
      2. Inside tags, the only changed tag is 'GitCommitHash'
    """

    changed_attributes = get_changed_attributes(before, after)

    if changed_attributes != {"tags"}:
        return False

    before_tags = before.get("tags") or {}
    after_tags = after.get("tags") or {}

    all_tags = set(before_tags.keys()) | set(after_tags.keys())

    changed_tags = {
        tag
        for tag in all_tags
        if before_tags.get(tag) != after_tags.get(tag)
    }

    return changed_tags == {"GitCommitHash"}


def validate_plan(plan):
    """
    Validate all resource changes in a Terraform JSON plan.
    """

    resource_changes = plan.get("resource_changes", [])

    for resource in resource_changes:

        address = resource.get("address", "unknown")
        change = resource.get("change", {})
        actions = change.get("actions", [])

        # Nothing is changing.
        if actions == ["no-op"]:
            continue

        # Creating a resource is allowed.
        if actions == ["create"]:
            continue

        # Updating a resource is allowed only when
        # GitCommitHash is the only change.
        if actions == ["update"]:

            before = change.get("before")
            after = change.get("after")

            if only_git_commit_hash_changed(before, after):
                continue

            print("PLAN REJECTED")
            print(
                f"Action required: Do not apply the plan. "
                f"Resource '{address}' modifies attributes other than "
                f"tags.GitCommitHash."
            )
            return False

        # Delete, replacement, or any unexpected action is forbidden.
        print("PLAN REJECTED")
        print(
            f"Action required: Do not apply the plan. "
            f"Resource '{address}' has forbidden Terraform actions: "
            f"{actions}"
        )
        return False

    print("PLAN APPROVED")
    print("Action required: Terraform apply may proceed.")
    return True


def main():

    if len(sys.argv) != 2:
        print("Usage: python script.py <tfplan.json>")
        sys.exit(1)

    filename = sys.argv[1]

    try:
        with open(filename, "r", encoding="utf-8") as file:
            plan = json.load(file)

    except FileNotFoundError:
        print(f"ERROR: File not found: {filename}")
        sys.exit(1)

    except json.JSONDecodeError:
        print(f"ERROR: '{filename}' is not valid JSON.")
        sys.exit(1)

    approved = validate_plan(plan)

    if approved:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()