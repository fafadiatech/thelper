import requests
import operator
from collections import defaultdict

from config import TRELLO_KEY, TRELLO_TOKEN, BOARD_ID, API_BASE
from exporters import export_tsv, export_html
from utils import dict_to_list

# this will keep track of counts
label_counts = defaultdict(int)
members_card_counts = defaultdict(int)

# for given member id store member name
# this will avoid too many API calls
member_id_to_name_cached = {}


def get_trello_response(URL):
    """
    given a URL get response from Trello's REST API
    """
    response = requests.get(URL)
    if response.status_code == 200:
        return response.json()
    return {}


def get_member_name(member_id):
    """
    given member_id, get full name
    """
    if member_id in member_id_to_name_cached:
        return member_id_to_name_cached[member_id]

    MEMBER_URL = f"{API_BASE}members/{member_id}?key={TRELLO_KEY}&token={TRELLO_TOKEN}"
    member_info = get_trello_response(MEMBER_URL)
    if "fullName" in member_info:
        member_id_to_name_cached[member_id] = member_info["fullName"]
        return member_info["fullName"]
    return ""


def humanize(title, some_list):
    """
    this function is used to print reports on terminal
    """
    print(title)
    for row in some_list:
        print("\t", "\t".join(row))


def humanize_dict(title, some_dict):
    """
    this function is used to print report for a dictionary
    sorted by reverse order of values
    """
    sorted_some_dict = dict(
        sorted(some_dict.items(), key=operator.itemgetter(1), reverse=True)
    )
    report_rows = []
    for k, v in sorted_some_dict.items():
        row = [k, str(v)]
        report_rows.append(row)
    humanize(title, report_rows)


if __name__ == "__main__":
    LISTS_URL = (
        f"{API_BASE}boards/{BOARD_ID}/lists?key={TRELLO_KEY}&token={TRELLO_TOKEN}"
    )
    all_lists = get_trello_response(LISTS_URL)

    list_summary = []
    for current_list in all_lists:
        CARDS_URL = f"{API_BASE}lists/{current_list['id']}/cards?key={TRELLO_KEY}&token={TRELLO_TOKEN}"
        all_cards = get_trello_response(CARDS_URL)
        list_summary.append([current_list["name"], str(len(all_cards))])

        # this loop will count cards by labels
        for current_card in all_cards:
            for current_label in current_card["labels"]:
                label_counts[current_label["name"]] += 1

            for current_member_id in current_card["idMembers"]:
                member_name = get_member_name(current_member_id)
                members_card_counts[member_name] += 1

    context = {}
    humanize("\nList Summary Report:", list_summary)
    export_tsv("list-summary.tsv", list_summary)
    context["list_summary"] = list_summary

    humanize_dict("\nLabel Summary Report", label_counts)
    export_tsv("label-summary.tsv", label_counts, is_dict=True)
    context["label_counts"] = dict_to_list(label_counts)

    humanize_dict("\nMembers Summary Report", members_card_counts)
    export_tsv("members-summary.tsv", members_card_counts, is_dict=True)
    context["members_card_counts"] = dict_to_list(members_card_counts)

    export_html("report.html", context)
