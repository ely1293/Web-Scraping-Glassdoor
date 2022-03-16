# Import necessary libraries
# standard libraries
from time import time
# custom functions
try:
    from packages.common import requestAndParse
except ModuleNotFoundError:
    from common import requestAndParse


# extracts desired data from listing banner
def extract_listingBanner(listing_soup):
    listing_bannerGroup_valid = False

    try:
        listing_bannerGroup = listing_soup.find("div", class_="css-ur1szg e11nt52q0")
        listing_bannerGroup_valid = True

    except:
        print("[ERROR] Error occurred in function extract_listingBanner")
        Company = "NA"
        Rating = "NA"
        Role = "NA"
        Location = "NA"
        Salary = "NA"
    
    if listing_bannerGroup_valid:
        try:
            Rating = listing_bannerGroup.find("span", class_="css-1pmc6te e11nt52q4").getText()
        except:
            Rating = "NA"
        if Rating != "NA":
            try:
                Company = listing_bannerGroup.find("div", class_="css-16nw49e e11nt52q1").getText().replace(Rating,'')
            except:
                Company = "NA"
            Rating = Rating[:-1]
        else:
            try:
                Company = listing_bannerGroup.find("div", class_="css-16nw49e e11nt52q1").getText()
            except:
                Company = "NA"

        try:
            Role = listing_bannerGroup.find("div", class_="css-17x2pwl e11nt52q6").getText()
        except:
            Role = "NA"

        try:
            Location = listing_bannerGroup.find("div", class_="css-1v5elnn e11nt52q2").getText()
        except:
            Location = "NA"
        try:
            Salary = listing_bannerGroup.find("span", class_="css-1jd3gb2 e1v3ed7e0").next_sibling.strip()
        except:
            Salary = "NA"

    return companyName, company_starRating, company_offeredRole, company_roleLocation, Salary

def extract_listingInsights(listing_soup):
    listing_Insights_valid = False

    try:
        listing_Insights = listing_soup.find("div", class_="css-1x772q6 e18tf5om0")
        listing_Insights_valid = True
    except:
        print("[ERROR] Error occurred in function extract_listingInsights")
        JobType = "NA"
        JobFunction = "NA"
        Industry = "NA"
        Size = "NA"

    if listing_Insights_valid:
        try:
            JobType = listing_Insights.find("span", class_="css-sr4ps0 e18tf5om4").getText()
        except:
            JobType = "NA"
        try:
            JobFunction = listing_Insights.find("span", class_="css-o4d739 e18tf5om4").getText()
        except:
            JobFunction = "NA"
        try:
            Industry = listing_Insights.find_all("span", class_="css-sr4ps0 e18tf5om4")[1].get_text().strip()
        except:
            Industry = "NA"
        try:
            Size = listing_Insights.find_all("span", class_="css-sr4ps0 e18tf5om4")[2].get_text().strip()
        except:
            Size = "NA"

    return JobType, JobFunction, Industry, Size

# extracts desired data from listing description
def extract_listingDesc(listing_soup):
    extract_listingDesc_tmpList = []
    listing_jobDesc_raw = None

    try:
        listing_jobDesc_raw = listing_soup.find("div", id="JobDescriptionContainer")
        if type(listing_jobDesc_raw) != type(None):
            JobDescriptionContainer_found = True
        else:
            JobDescriptionContainer_found = False
            Description = "NA"
    except Exception as e:
        print("[ERROR] {} in extract_listingDesc".format(e))
        JobDescriptionContainer_found = False
        Description = "NA"

    if JobDescriptionContainer_found:
        jobDesc_items = listing_jobDesc_raw.findAll('li')
        for jobDesc_item in jobDesc_items:
            extract_listingDesc_tmpList.append(jobDesc_item.text)

        Description = " ".join(extract_listingDesc_tmpList)

        if len(Description) <= 10:
            Description = listing_jobDesc_raw.getText()

    return Description


# extract data from listing
def extract_listing(url):
    request_success = False
    try:
        listing_soup, url = requestAndParse(url)
        request_success = True
    except Exception as e:
        print("[ERROR] Error occurred in extract_listing, requested url: {} is unavailable.".format(url))
        return ("NA", "NA", "NA", "NA", "NA", "NA", "NA", "NA", "NA", "NA", "NA")

    if request_success:
        Company, Rating, Role, Location, Salary = extract_listingBanner(listing_soup)
        JobType, JobFunction, Industry, Size = extract_listingInsights(listing_soup)
        Description = extract_listingDesc(listing_soup)

        return (Company, Rating, Role, Location, Salary, JobType, JobFunction, Industry, Size, Description, url)


if __name__ == "__main__":
    
    url = "https://www.glassdoor.sg/job-listing/senior-software-engineer-java-scala-nosql-rakuten-asia-pte-JV_KO0,41_KE42,58.htm?jl=1006818844403&pos=104&ao=1110586&s=58&guid=00000179d5112735aff111df641c01be&src=GD_JOB_AD&t=SR&vt=w&ea=1&cs=1_c8e7e727&cb=1622777342179&jobListingId=1006818844403&cpc=AF8BC9077DDDE68D&jrtk=1-1f7ah29sehimi801-1f7ah29t23ogm000-80a84208d187d367&jvt=aHR0cHM6Ly9zZy5pbmRlZWQuY29tL3JjL2dkL3BuZz9hPUh5MlI4ekNxUWl3d19sM3FuaUJHaFh3RlZEYUJyUWlpeldIM2VBR1ZHTUVSeUk5VEo1ZTEzWWl5dU1sLWJWX0NIeGU4NjBDc3o0dE5sV3ZLT2pRTHFIZU5KTHpPLUhLeEFRSERmeE5CdHNUTUc1RV9FSFR2VW5FNldmWWxJQVp5dXIzNFRZZjIzLWNWNXE0NnRhSTF3V1pKeW54dHhNUkxVRlhEekI2djYwMVZGWl9vbGU5andSYjVhX3BvT0cza0JJb0NYQXo0TVZhNWdvUFY4dXY3WVJTYlMySUpZTVpyR252dEc3ZFM1aXlFQ09icHI0YVRKU2ZLUzkzMUxmLXpyQjFlZHZxbHBxbElZMXhpRksxZmdIMEhFLTJBN2pySHRZa1g0aDJCWGRxTzBCdDM0bDNzWlJDLWIxaUlCT0xnZFh6bjg4cnNjZ1N0V1BHdVhNVm5xT3A3Q0s1UEEtb0QxWDl0WFhkY19WM3Fic0dSS0tfZi1oVUZyUUlrc0o2ZV9yVHNjaFpRVkIyV2V1bmRBejNYQWVPcFZNb3lqZFlONWpLUTdVbDUxTlU5LXFVWnZIT19VWlNEWDVtdVYwR3dNbWpXVDFyaHhMM3ZkcUZqcnM4WDZuc3BYYUhYcHg1dXNUVTVJODdzQk12Q2owaXkxTmRjUmhNXzU2TF9KbXNlY0VzajNWWmFOMDQ3QmNSWU5HSGNFNmctcXUzRUV4bHJrdjQxQ3QteW02ZFo5bE45XzBfb3prR2NBVkdqQU9kaS1UNWRwVnllYzA1OU53Q3Aya2QwdHdoRU5kUnU5UzNlTUR5WmJOSFZGb0t3MnR6V1lKbTllaGxuS3hTMEdoMDhLekVBWGg4OW9BblZGR2U2ajRtMUw3T29CSVNvZWVZaC0wRHRoSTV4eUV0ODJCRERkeTV3QlREUVNTUUZ1Mkp3WUEyRE9qZk5udk5xbzQwaVZKRmF0VWFlVDc2TFl6bnIwQTB2RWRGZlNORE41QmlUaHI3VmgyUWs3bkRGaVFibmUzcWlqZE1ZYzR5TmVYZUhnUFFmOHEwc1Q2aHJrX0hPX1RwbWI5M21hd2hxOEd6a2lEaFMtUQ&ctt=1622777391568"
    start_time = time()
    returned_tuple = extract_listing(url)
    time_taken = time() - start_time
    print(returned_tuple)
    print("[INFO] returned in {} seconds".format(time_taken))