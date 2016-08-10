import argh
from redmine import Redmine
from github3 import login

issue_categories = {
    u'agendav': 9,
    u'baikal': 10,
    u'dokuwiki': 11,
    u'general': 47,
    u'hextris': 12,
    u'jappix': 13,
    u'jirafeau': 14,
    u'kanboard': 31,
    u'my_webapp': 15,
    u'opensondage': 16,
    u'openvpn': 17,
    u'owncloud': 18,
    u'phpmyadmin': 19,
    u'roundcube': 20,
    u'searx': 21,
    u'shellinabox': 22,
    u'strut': 23,
    u'transmission': 24,
    u'ttrss': 25,
    u'wallabag': 26,
    u'wallabag2': 64,
    u'wordpress': 27,
    u'zerobin': 28,
}

def main(user, repo, redmine_key, github_login, github_password):
    g = login(github_login, github_password)
    r = Redmine('https://dev.yunohost.org', key=redmine_key)
    p = r.project.get('apps')

    issue_categorie_id = issue_categories[repo.replace("_ynh", "").lower()]

    for issue in g.iter_repo_issues(user, repo, state="open"):
        if issue.pull_request:
            continue

        subject = issue.title
        description = issue.body_text
        user = issue.user.login

        description = "**Imported from %s, reported by [@%s](%s) on %s**\n\n" % (issue.html_url, user, issue.user.html_url, issue.updated_at.strftime("%X %F")) + description

        for comment in issue.iter_comments():
            description += "\n------------------------------------------------------------------------------------------\n\n"\
                           "**Comment by [%s](%s) on %s**\n\n" % (comment.user.login, comment.user.html_url, comment.updated_at.strftime("%X %F"))

            description += comment.body_text

        print 'Importing: "%s"' % subject
        new_issue = p.issues.manager.create(subject=subject, description=description, categorie_id=issue_categorie_id, project_id=p.id)

        url = "https://dev.yunohost.org/issues/%s" % new_issue.id

        issue.create_comment("Issue migrated at %s\n\nIt would be great if you could use this bugtracker instead of github from now one :) (you don't have to create an account and you can log with github)" % url)
        issue.close()


if __name__ == '__main__':
    argh.dispatch_command(main)
