


def get_adm_count(group_id, adm_count):
    pass


def check_adm_count_change(group_id, adm_count):
    pass


def send_alert(group_id, adm_count):
    pass


def send_to_es(group_id, adm_count):
    pass



def main():
    group_id = 123
    adm_count = get_adm_count(group_id)
    adm_count_change = check_adm_count_change(group_id, adm_count)
    if adm_count_change:
        send_alert(group_id, adm_count)
    send_to_es(group_id, adm_count)



if __name__ == '__main__':
    main()
