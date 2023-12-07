def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if True: #iteration == total: 
        print()
        
def progress_bar(total,prefix = 'Progress:'):
    printProgressBar(0, total, prefix, suffix = 'Complete', length = 50)
    def progress(): 
        for i in range(total):
            yield
            print("continue")
            time.sleep(0.1)
            # Update Progress Bar
            printProgressBar(i + 1, total, prefix, suffix = 'Complete', length = 50)
    return progress


prog =  progress_bar(50)
for i in range(100000000000000):
    if i %10000==0:
        next(prog())
        
        # print("hit")