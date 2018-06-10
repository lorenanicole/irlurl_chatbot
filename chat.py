
class Script(object):

    collected_data = {
        'name': None,
        'zipcode': None,
        'email': None,
        'phone_number': None,
        'interests': None,
        'notes': None
    }

    def __init__(self, question_order):
        self.question_order = question_order

    def welcome(self):
         return(self.question_order.opening_script_question.text)


class AdelitaBot(object):
    def __init__(self, script):
        self.script = Script(question_order)
        self.outbound_webhook_url = 'https://hooks.slack.com/services/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'
        self.inbounc_webhook_url = 'https://hooks.slack.com/services/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'

    def send_msg(self, text):
        response = requests.post(
            self.outbound_webhook_url,
            data=json.dumps(text),
            headers={'Content-Type': 'application/json'}
        )

    def chat(self):
        self.send_msg(self.script.welcome())

        for question in self.script.question_order:

            for indx, text in enumerate(question.text):
                if question.format and question.format[indx]:
                    text = text.format(self.script.collected_data[question.format[indx]])

                self.send_msg(text)

                if '?' in text:
                    if question.options:
                        self.send_msg('Options:')
                        for option in question.options:
                            self.send_msg(option)

                    statement = input("> ").lower()

                    if self.script.collected_data.get(question.data):
                        self.script.collected_data[question.data] = statement

                if statement == "quit" or statement == "bye":
                    break

        return