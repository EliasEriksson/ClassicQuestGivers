def parse_series(selector, quest):
    if selector:
        # if its a chain quest
        if selector.xpath('tr/th[contains(text(), "1.")]/../td/div/b'):
            # current quest is the first in series, no series requirements
            pass
        elif selector.xpath('tr/th[contains(text(), "1.")]/../td/div/span/b'):
            # current quest is the firs quest in the series, no series requirements
            pass
        else:
            previous_quest = selector.xpath('tr/td/div/b/../../../preceding-sibling::tr[1]/td/div/a')
            if previous_quest:
                # previous non faction specific quest
                pass
            else:
                if quest["faction"] == "A":
                    # if previous quest is alliance specific
                    previous_quest = selector.xpath(
                        'tr/td/div/span/b/../../../../preceding-sibling::tr[1]/'
                        'td/span[@class="icon-alliance-padded"]/a')
                    if previous_quest:
                        pass
                elif quest["faction"] == "H":
                    previous_quest = selector.xpath(
                        'tr/td/div/span/b/../../../../preceding-sibling::tr[1]/'
                        'td/span[@class="icon-horde"]/a')
                    if previous_quest:
                        pass
                elif quest["faction"] == "N":
                    previous_quests = selector.xpath(
                        'tr/td/div/span/b/../../../../preceding-sibling::tr[1]/'
                        'td/span/a')
                    if previous_quest:
                        pass