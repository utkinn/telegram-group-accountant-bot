Я BOT_NAME. Я здесь, чтобы помочь вам учитывать расходы на мероприятия и распределять их по участникам.
Я понимаю следующие команды:

/help@BOT_USER_NAME — отображение этой справки
/new@BOT_USER_NAME Настолки — я создам новый сбор с названием “Настолки” и буду заносить туда все последующие траты.
/spend@BOT_USER_NAME Ром 100 — я запишу, что вы потратили 100 рублей на ром в рамках текущего сбора. Если сбор не был объявлен, я создам его сам.
/spend@BOT_USER_NAME Ром 100 @foo — я запишу, что @foo потратил 100 рублей на ром в рамках текущего сбора. Если сбор не был объявлен, я создам его сам.
/rename@BOT_USER_NAME Новое имя — я дам текущему сбору новое имя.
/info@BOT_USER_NAME — я напишу информацию про текущий сбор.
/count@BOT_USER_NAME @foo @bar @baz — я распределю траты поровну на указанных пользователей.
/cancel@BOT_USER_NAME — я отменю или закрою текущий сбор.
