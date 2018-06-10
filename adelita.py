from collections import namedtuple

import sys

Question = namedtuple('Question', 'text format options order data')


opening_text = ['''Hola! Thanks for joining. I'm Adelita, the Mijente AI Organizer. How are you?''']

permission_to_talk_text = ['''We’re excited to have you be a part of Mijente -- building our political casita together starts with knowing what sort of tools we all have available.  We’re trying to get a sense of our members’ interests to see where you want to plug in. Is it okay if I ask you some questions so one of our organizers can follow up with you?''']

name_text = ['''Great! I’m excited to get to know more about you.''', '''Let’s start with your contact info. What’s your name?''']

email_text = ['''And your e-mail?''']

phone_number_text = ['''K, and your phone number? Sometimes we send text alerts for actions!''']

zipcode_text = ['''Thanks. What’s your zip code? We want to make sure to connect you with local Mijenterxs.''']

interests_text = ['''Ah, entonces estas en Chicago]! Got it.''',
                  '''Now, tell me a little about your interests. Mijente is a political home for Latinx people who are pro-black, pro-queer, pro-poor because our community is all that and more.''',
                  '''What are some issues that are important to you? You can say things like “art, technology, direct action, reproductive justice” and I’ll make some notes!''']

issues_text = ['''Gracias.''', '''Mijenterxs are doing dope things all over the country. Some of us are Communications or tech people, healing justice folks, interpreters/translators -- de todo. Any of that sound interesting?''']

comms_text = ['''Our Commsquad creates and amplifies content that tells our members’ stories.''', '''Sometimes that means making graphics for campaigns''', '''Image''', '''… or livestreaming an action, and other times it means writing a blog post to share your perspective on an issue.''',
 '''Te parece bien?''']

etc_interests = ['''Dale, entonces we’ll make sure you get connected to someone from the Commsquad. Look out for a text or e-mail soon!''']

closing_text = ['''Thanks for sharing a bit about yourself. I enjoyed chatting with you! ''']

quit_text = 'Ok. Come back anytime if you have questions!'

opening_script_question = Question(text=opening_text, format=None, options=[], order=1, data='name')

question_order = [
    Question(text=permission_to_talk_text, format=None, options=[], order=2, data=None),
    Question(text=name_text, format=None, options=[], order=3, data='email'),
    Question(text=email_text, format=None, options=[], order=4, data='email'),
    Question(text=phone_number_text, format=[], options=[], order=5, data='phone_number'),
    Question(text=zipcode_text, format=None, options=[], order=6, data='zipcode'),
    Question(text=interests_text, format=['zipcode', None, None], options=[], order=7, data='interests'),
    Question(text=issues_text, format=None, options=['Communications', 'Healing Justice', 'Language Justice'], order=8, data=None),
    Question(text=comms_text, format=None, options=[], order=9, data=None),
    Question(text=etc_interests, format=None, options=['Interests'], order=10, data=None),
    Question(text=closing_text, format=None, options=[], order=11, data=None)
]


class Profile(object):
    data_points = [
        'name', 'zipcode', 'email', 'phone_number', 'interests', 'notes'
    ]

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            if k not in self.data_points:
                raise Exception('{} not supported'.format(k))

            setattr(self, k, v)

    def __str__(self):
        return 'Mijente Profile: \nName: {}\nZipcode: {}\nEmail: {}\nPhone: {},\n Interests: {},\n Notes: {}'.format(self.name, self.zipcode, self.email, self.phone_number, self.interests, self.notes)



def main():

    collected_data = {
        'name': None,
        'zipcode': None,
        'email': None,
        'phone_number': None,
        'interests': None,
        'notes': None
    }

    print(opening_script_question.text)

    statement = input("> ").lower()

    for question in question_order:

        for indx, text in enumerate(question.text):
            if question.format and question.format[indx]:
                text = text.format(collected_data[question.format[indx]])

            print(text)

            if '?' in text:
                if question.options:
                    print('Options:\n')
                    for option in question.options:
                        print('{}'.format(option))

                statement = input("> ").lower()

                if collected_data.get(question.data):
                    collected_data[question.data] = statement

            if statement == "quit" or statement == "bye":
                sys.exit()

    user_profile = Profile(**collected_data)
    print(user_profile)

if __name__ == "__main__":
    main()