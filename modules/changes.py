import library.beachdoglib as library

def main():
    def sw1(scr: int) -> int:
        switch = {5: 20, 10: 20, 15: 20, 20: 30, 25: 40, 30: 30, 50: 50, 60: 60, 80: 70}
        return switch.get(scr, 0)

    def sw2(scr: int) -> int:
        switch = {20: 0, 30: 1, 40: 2, 50: 3, 60: 4, 70: 5}
        return switch.get(scr, 0)

    # Initialize the score grid and counters
    inc, dec, unc = [0] * 6, [0] * 6, [0] * 6
    sc = [[0] * 6 for x in range(6)]

    # Load dictionaries
    mDict = library.myDict(min_score=0)
    jDict = library.xwiDict(min_score=0)

    # Main loop to compare scores
    for word in jDict:
        if word in mDict:
            newScore = sw1(jDict[word])
            jSw, mSw = sw2(newScore), sw2(mDict[word])
            
            sc[jSw][mSw] += 1
            
            # Track score changes
            if mDict[word] > newScore:
                inc[jSw] += 1
            elif mDict[word] < newScore:
                dec[jSw] += 1
            else:
                unc[jSw] += 1

    # Calculate totals
    decreasedTotal, unchangedTotal, increasedTotal = sum(dec), sum(unc), sum(inc)
    total = decreasedTotal + unchangedTotal + increasedTotal
    changed = decreasedTotal + increasedTotal
    percent = changed / total * 100 if total else 0

    # Initialize output text string
    message = ''

    # Output header
    message += f'CHANGES IN SCORE FROM JEFF\'S LIST\n\n'
    message += f'  OLD  {'-'*36} NEW SCORE {'-'*36}\n'
    message += f'SCORE        20       30       40       50       60       70       80       DEC       UNC       INC\n'
    message += f'  {'-'*5} {'-'*83}\n'

    # Output the table of scores
    for k in range(6):
        message += f'{k * 10 + 20: 5} '
        for e in range(6):
            message += f'{sc[k][e]: 9}'
        message += f'{dec[k]: 9} {unc[k]: 9} {inc[k]: 9}\n'
    message += f' {'-'*5}  {'-'*83}\n'

    # Output totals
    message += (
        f'TOTAL {changed: 9} changes out of {total: {len(str(total)) + 1}} processed '
        f'({percent:2>1%}){decreasedTotal: 13} {unchangedTotal: 9}'
        f'{increasedTotal: 10}\n\n'
        )
    return message

# Entry point of the script
if __name__ == "__main__":
    main()
