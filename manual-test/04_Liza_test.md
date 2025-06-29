### TC-25: Оповещение при успешном переводе

**Cтатус:** OK

**Предусловия:**
Все данные введены корректно

**Шаги:**
- Ввести валидный номер карты и сумму перевода в рамках доступной суммы.
- Нажать 'Перевести'.
- Убедиться, что появляется уведомление об успешной отправке запроса.

**Ожидаемый результат:**
Появляется сообщение об успешной отправке

---

### TC-26: Проверка кнопки перевода при пустом поле суммы

**Cтатус:** FAIL

**Предусловия:**
Номер карты введён

**Шаги:**
- Выбрать рубли, ввести номер карты.
- Оставить поле суммы пустым.
- Убедиться, что кнопка 'Перевести' неактивна.

**Ожидаемый результат:**
Кнопка неактивна

---

### TC-27: Ошибка при передаче отрицательных значений баланса через URL

**Cтатус:** FAIL (По правилам ТЗ)

**Предусловия:**
Переданы значения ?balance=-1000&reserve=0

**Шаги:**
- Открыть страницу с URL ?balance=-1000&reserve=0.
- Проверить отображение баланса на главной странице.

**Ожидаемый результат:**
Ошибка отображения — баланс не должен быть отрицательным.

---

### TC-28: Перевод малой суммы 

**Cтатус:** FAIL 

**Предусловия:**
- Баланс на счёте: 100₽
- Резерв: 0₽
- Тестовый номер карты: 1111 1111 1111 1111
- Сумма перевода: 10₽


**Шаги:**
1.	Открыть страницу с URL
2.	Выбрать рублёвый счёт.
3.	Ввести номер карты
4.	Ввести сумму перевода
5. Нажать кнопку перевести

**Ожидаемый результат:**
Кнопка “Перевести” должна отображаться.
Никаких сообщений об ошибке быть не должно, так как 10₽ + 1₽ комиссии укладываются в 100₽.
Перевод доступен к выполнению.

---

### TC-29: Перевода всей суммы с рублёвого счёта

**Cтатус:** OK 

**Предусловия:**
- Баланс на счёте: 10000₽
- Резерв: 0₽
- Тестовый номер карты: 1111 1111 1111 1111
- Сумма перевода: 10000₽


**Шаги:**
1.	Открыть страницу с URL
2.	Выбрать рублёвый счёт.
3.	Ввести номер карты
4.	Ввести сумму перевода
5. Нажать кнопку перевести

**Ожидаемый результат:**
Появляется сообщение об ошибке: “Недостаточно средств на счёте”,
так как сумма перевода + комиссия (1000₽ + 100₽) превышает доступный баланс.
Кнопка “Перевести” не отображается.

---


### TC-30: Перевода всей суммы с долларового счёта

**Cтатус:** FAIL 

**Предусловия:**
- Баланс на счёте: 10000₽
- Резерв: 0₽
- Тестовый номер карты: 1111 1111 1111 1111
- Сумма перевода: 100$


**Шаги:**
1.	Открыть страницу с URL
2.	Выбрать долларовый счёт.
3.	Ввести номер карты
4.	Ввести сумму перевода
5. Нажать кнопку перевести

**Ожидаемый результат:**
Появляется сообщение об ошибке: “Недостаточно средств на счёте”,
так как сумма перевода + комиссия (100$ + 10$) превышает доступный баланс.
Кнопка “Перевести” не отображается.


