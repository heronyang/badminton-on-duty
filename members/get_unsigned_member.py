with open('now_members.txt', 'r') as now_members_file:
    now_members = set(now_members_file.read().split())

with open('signed_members.txt', 'r') as signed_members_file:
    signed_members = set([name[1:].lower()
                         for name in signed_members_file.read().split()])

print('[Unsigned Memeber]')
for name in (now_members - signed_members):
    print(name)

print('[Surprised Memeber]')
for name in (signed_members - now_members):
    print(name)
