def select(response):
    infobox = response.xpath('//*[@id="infobox-alternate-position"]/table')
    return infobox.xpath('//th[@id="infobox-series"]/../../tr/td//table[@class="series"]/tbody')


def parse(selector, quest):
    if selector:
        # if its a chain quest
        if selector.xpath('tr/th[contains(text(), "1.")]/../td/div/b'):
            # current quest is the first in series, no series requirements
            print("Current quest is the first in a series of quests, no requirement thru series required.")
            pass
        elif selector.xpath('tr/th[contains(text(), "1.")]/../td/div/span/b'):
            # current quest is the firs quest in the series, no series requirements
            print("Current quest is the first in a series of quests, no requirement thru series required.")
            pass
        else:
            previous_quest = selector.xpath('tr/td/div/b/../../../preceding-sibling::tr[1]/td/div/a')
            if previous_quest:
                print("Previous quest is a non faction specific quest")
                # previous non faction specific quest
                pass
            else:
                if quest["faction"] == "A":
                    # if previous quest is alliance specific
                    previous_quest = selector.xpath('tr/td/div/span/b/../../../../preceding-sibling::tr[1]'
                                                    '/td/div/span[@class="icon-alliance-padded"]/a')
                    if previous_quest:
                        print("Previous quest is an alliance specific quest.")
                    else:
                        print("Previous quest shouldve been detected as alliance quest or something else.")
                elif quest["faction"] == "H":
                    previous_quest = selector.xpath(
                        'tr/td/div/span/b/../../../../preceding-sibling::tr[1]/'
                        'td/div/span[@class="icon-horde"]/a')
                    if previous_quest:
                        print("Previous quest is a horde specific quest.")
                    else:
                        print("Previous quest shouldve been a horde specific quest or something else.")
                else:
                    print("wtf went wrong.")


quest = {"faction": ""}
