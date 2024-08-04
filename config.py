from dotenv import load_dotenv
import os

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
GREETINGS = '''👋 Привет! Я бот-администратор тату салона.
С моей помощью ты сможешь выбрать себе мастера и записаться на сеанс! 📆'''
ADDRESS = 'Наша студия находится по адресу г.Москва, Цветной Бульвар, д. **'
ABOUT_US = '''❤️‍🔥Мы - команда профессиональных тату-мастеров, с горячим сердцем и творческим умом, готовые воплотить ваши идеи в живые произведения искусства на вашей коже.

☑️Наша миссия - создавать не просто татуировки, а уникальные истории, которые олицетворяют вашу индивидуальность и стиль. Мы ценим каждого нашего клиента и стремимся к тому, чтобы ваше посещение нашего салона было незабываемым и комфортным.

🧴В нашем салоне вы найдете не только профессиональных мастеров, но и безопасные условия, строгий контроль за гигиеной, а также дружественную атмосферу, где каждый чувствует себя как дома.

🙌Присоединяйтесь к нам и доверьте свои идеи нашим талантливым мастерам - вместе мы создадим татуировку, которая будет радовать вас всю жизнь.'''