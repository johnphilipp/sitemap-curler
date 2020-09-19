import webbrowser
import subprocess
import os.path
import pathlib
import requests

# EXIT FUNCTION
def exitProgram():
    print("\nProgram finished.\n")
    f.close()
    exit()


# DOWNLOAD SITEMAP.XML FROM USER SPECIFIED URL
url = input("Please enter full URL to sitemap: ")

response = requests.get(url)
with open("sitemap.xml", "wb") as file:
    file.write(response.content)


# OPEN SITEMAP.XML
f = open("sitemap.xml", "r")
content = f.read()

print("\nFound {} characters in sitemap".format(len(content)))
print("Crawling...\n")


# CRAWL URL FOR LINKS
linkRepo = []

for i in range(0, len(content)):
    if content[i : i + 5] == "<loc>":
        startOfLink = i + 5

        for j in range(0, len(content) - i):
            if content[i + j : i + j + 6] == "</loc>":
                endOfLink = i + j
                break
        link = content[startOfLink:endOfLink]
        linkRepo.append(link)

for i in range(0, len(linkRepo)):
    print(i + 1, linkRepo[i])

print("\nFinished crawling. Found {} links.".format(len(linkRepo)))


# OPTIONAL FOLLOW UP #1: SAVE URLS TO FILE
followUpSaveToFile = input("\nDo you want to save the links to a file? (y/n) ")

if followUpSaveToFile == "y":
    linkFileName = input("""\nPlease specify filename (e.g. "links.txt"): """)

    print("Writing file {}...".format(linkFileName))

    with open(linkFileName, "w") as filehandle:
        for listitem in linkRepo:
            filehandle.write("%s\n" % listitem)

    openFile = os.path.join(pathlib.Path(__file__).parent.absolute(), linkFileName)
    subprocess.call(["open", openFile])

    print("Finished writing file.")


# OPTIONAL FOLLOW UP #2: OPEN URLS (ALL OR RANGE) IN BROWSER
followUpOpenInBrowser = input("\nDo you want to open the links in your browser? (y/n) ")

if followUpOpenInBrowser == "y":
    howManyWindows = input("\nAll of them? (y/n) ")

    if howManyWindows == "y":

        def openAllWindows(linkRepo=linkRepo):
            print("\nOpening all windows...")

            for i in range(0, len(linkRepo)):
                webbrowser.open(linkRepo[i], new=2)

            print("Finished opening windows.")

        openAllWindows()

    elif howManyWindows == "n":

        def rangeSpec():
            rangeSpec.rangeFrom = int(input("\nSpecify range - From? "))
            rangeSpec.rangeTo = int(input("\nSpecify range - To? "))

            return rangeSpec.rangeFrom, rangeSpec.rangeTo

        rangeSpec()

        def rangeValidation(rangeFrom=rangeSpec.rangeFrom, rangeTo=rangeSpec.rangeTo):
            if rangeFrom < 0 or rangeTo < 0 or rangeTo - rangeFrom < 0:
                print("\nError: Please enter valid range")
                rangeSpec()

        rangeValidation()

        def openRangeWindows(
            rangeFrom=rangeSpec.rangeFrom, rangeTo=rangeSpec.rangeTo, linkRepo=linkRepo
        ):
            print("\nOpening specified window range...")

            for i in range(rangeSpec.rangeFrom - 1, rangeSpec.rangeTo):
                webbrowser.open(linkRepo[i], new=2)

            print("Finished opening windows.")

        openRangeWindows()

exitProgram()