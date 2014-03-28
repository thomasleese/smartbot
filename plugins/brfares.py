import io
import re
import requests
import unittest
import urllib.parse


class Plugin:
    names = ["fares", "brfares"]
    def __init__(self):
        self.saved_items = {}
        self.up_to = 0

    def get_code(self, req_url, orig_string, headers, payload, stdout):
        res = requests.get(req_url, headers=headers, params=payload).json()
        if len(res) == 0:
            print("No results for {0}!".format(orig_string), file=stdout)
            return None
        else:
            return res[0]["code"]
        

    def on_command(self, bot, msg, stdin, stdout, reply):
        pattern = r"(?:br)?fares (?:from )?(.*) to (.*?)(?: with (.*))?$"
        match = re.match(pattern, msg["message"], re.IGNORECASE)
        if match:
            station1 = match.group(1)
            station2 = match.group(2)
            rlc = match.group(3) or " " * 3 # three spaces == no railcard

            station_url = "http://api.brfares.com/ac_loc"
            rlc_url = "http://api.brfares.com/ac_rlc"
            query_url = "http://api.brfares.com/querysimple"
            restriction_url = "http://www.brfares.com/restrictionspec"

            headers = {"User-Agent": "SmartBot"}
            
            stn1_code = self.get_code(station_url, station1, headers, {"term": station1}, stdout)
            stn2_code = self.get_code(station_url, station2, headers, {"term": station2}, stdout)
            rlc_code = self.get_code(rlc_url, rlc, headers, {'term': rlc}, stdout)

            if not stn1_code or not stn2_code or not rlc_code:
                return

            query_payload = {
                "orig": stn1_code,
                "dest": stn2_code,
                "rlc" : rlc_code,
            }
            fares = requests.get(query_url, headers=headers, params=query_payload).json()
            if len(fares["fares"]) == 0:
                print('No fares from {orig[ticketname]} ({orig[code]}) to {dest[ticketname]} ({dest[code]}) with {railcard[name]} ({railcard[code]})!'.format(**fares), file=stdout)
                return
            self.saved_items = fares
            print('Fares from {orig[ticketname]} ({orig[code]}) to {dest[ticketname]} ({dest[code]}) with {railcard[name]} ({railcard[code]}):'.format(**fares), file=stdout)
            for i, fare in enumerate(fares["fares"]):
                if i >= 10:
                    print("'fares more' to continue", file=stdout)
                    self.up_to = 10
                    return
                print("[{0}] {1[ticket][code]} {1[ticket][tclass][desc]} {1[ticket][name]} route {1[route][name]} - £{2:.2f}{3}".format(i, fare, (fare["adult"]["fare"] / 100.0) if "fare" in fare["adult"] else 0.00, "" if "fare" in fare["adult"] else " - No adult fare"), file=stdout)
            self.up_to = 0
            
        else:
            pattern = r"(?:br)?fares ([0-9]+)"
            match = re.match(pattern, msg["message"], re.IGNORECASE)
            if match:
                fares = self.saved_items
                try:
                    fare = fares["fares"][int(match.group(1))]
                except (IndexError, ValueError):
                    return
                
                # Print out fare!
                fare_orig = fare["group_orig"] or fares["orig"]
                extraorig = "Travelcard " if (fare["group_orig"] and fare["travelcard_orig"]) or (not fare["group_orig"] and fares["travelcard_orig"]) else ""
                extraorig += "Zonal" if (fare["group_orig"] and fare["zonal_orig"]) or (not fare["group_orig"] and fares["zonal_orig"]) else ""
                fare_dest = fare["group_dest"] or fares["dest"]
                extradest = "Travelcard " if (fare["group_dest"] and fare["travelcard_dest"]) or (not fare["group_dest"] and fares["travelcard_dest"]) else ""
                extradest += "Zonal" if (fare["group_dest"] and fare["zonal_dest"]) or (not fare["group_dest"] and fares["zonal_dest"]) else ""
                restricttrain = "" if fare["ticket"]["restr_train"] else "not "
                restrictdate = "" if fare["ticket"]["restr_date"] else "not "
                restrictarea = "" if fare["ticket"]["restr_area"] else "not "
                validityperiod = \
                    "" if fare["ticket"]["min_validity"] == 0 and fare["ticket"]["max_validity"] == 0 else \
                    (", valid {0} days".format(fare["ticket"]["min_validity"]) if fare["ticket"]["min_validity"] == fare["ticket"]["max_validity"] else \
                    ", valid {0}-{1} days".format(fare["ticket"]["min_validity"], fare["ticket"]["max_validity"]))
                adultminfarewarning = \
                    "- Minimum fare of £{:.2f} may apply".format(fare["adult"]["min_fare"]/100.0) if "min_fare" in fare["adult"] else \
                    ""
                childminfarewarning = \
                    "- Minimum fare of £{:.2f} may apply".format(fare["child"]["min_fare"]/100.0) if "min_fare" in fare["child"] else \
                    ""
                restrurl="www.nationalrail.co.uk/pdfs/{0}_{1}.pdf".format(fare["ticket"]["code"], fare["restriction_code"]) if fare["restriction_code"] != " " * 2 else ""


                out_string = \
'''Origin: {orig} ({origcode}) {extraorig}
Destination: {dest} ({destcode}) {extradest}
Fare: {fclass} ({classcode}) {name} ({namecode})
Fare type: {ftype} ({typecode})
Route: {route} ({routecode})
Cross-London Transfer: {maltese} ({maltesecode}) - please note that this only affects barrier acceptance, not actual ticket validity!
Fare Setter: {setter} ({settercode})
Fare validity: {validity} ({validitycode}), {restricttrain}restricted to a train, {restrictdate}restricted to a date, {restrictarea}restricted to an area{validityperiod}
Reservations required: {reservations} ({reservationscode})
Validity restriction code: {restrictions} {restrurl}
{adultname} ({adultcode}): £{adultprice:.2f} {adultminfarewarning}
{childname} ({childcode}): £{childprice:.2f} {childminfarewarning}
'''.format(
                    orig=fare_orig["longname"], origcode=fare_orig["code"], extraorig=extraorig,
                    dest=fare_dest["longname"], destcode=fare_dest["code"], extradest=extradest,
                    fclass=fare["ticket"]["tclass"]["desc"], classcode=fare["ticket"]["tclass"]["code"], name=fare["ticket"]["longname"], namecode=fare["ticket"]["code"],
                    ftype=fare["ticket"]["type"]["desc"], typecode=fare["ticket"]["type"]["code"],
                    route=fare["route"]["longname"], routecode=fare["route"]["code"],
                    maltese=fare["london_code"]["desc"], maltesecode=fare["london_code"]["code"],
                    setter=fare["fare_setter"]["name"], settercode=fare["fare_setter"]["code"],
                    validity=fare["ticket"]["validity"]["desc"], validitycode=fare["ticket"]["validity"]["code"], restricttrain=restricttrain, restrictdate=restrictdate, restrictarea=restrictarea, validityperiod=validityperiod,
                    reservations=fare["ticket"]["reservations"]["desc"], reservationscode=fare["ticket"]["reservations"]["code"],
                    restrictions=fare["restriction_code"] if fare["restriction_code"] != " " * 2 else "No restrictions", restrurl=restrurl,
                    adultname=fare["adult"]["status"]["name"] if "status" in fare["adult"] else "No adult fare", adultcode=fare["adult"]["status"]["ticket_code"] if "status" in fare["adult"] else "", adultprice=fare["adult"]["fare"] / 100.0 if "fare" in fare["adult"] else 0.0, adultminfarewarning=adultminfarewarning,
                    childname=fare["child"]["status"]["name"] if "status" in fare["child"] else "No child fare", childcode=fare["child"]["status"]["ticket_code"] if "status" in fare["child"] else "", childprice=fare["child"]["fare"] / 100.0 if "fare" in fare["child"] else 0.0, childminfarewarning=childminfarewarning)
                

                print(out_string, file=stdout)
            else:
                pattern = "(?:br)?fares more"
                match = re.match(pattern, msg["message"], re.IGNORECASE)
                if match and self.up_to > 0:
                    fares = self.saved_items
                    for i, fare in enumerate(fares["fares"][self.up_to:], start=self.up_to):
                        if i >= 10 + self.up_to:
                            print("'fares more' to continue", file=stdout)
                            self.up_to += 10
                            return
                        print("[{0}] {1[ticket][code]} {1[ticket][tclass][desc]} {1[ticket][name]} route {1[route][name]} - £{2:.2f}{3}".format(i, fare, (fare["adult"]["fare"] / 100.0) if "fare" in fare["adult"] else 0.00, "" if "fare" in fare["adult"] else " - No adult fare"), file=stdout)
                    self.up_to = 0
                else:
                    print(self.on_help(), file=stdout)

    def on_help(self):
        return "Usage: fares [from] <station> to <station> [with <railcard>]"


class Test(unittest.TestCase):
    def setUp(self):
        self.plugin = Plugin()

#    def test_status(self):
#        stdout = io.StringIO()
#        self.plugin.on_command(None, {"args": [None, "fares"]}, None, stdout, None)
#        self.assertFalse(stdout.getvalue().startswith("No such action"))
#        self.assertNotEqual(self.plugin.on_help(), stdout.getvalue().strip())

    def test_help(self):
        self.assertTrue(self.plugin.on_help())

    def test_no_args(self):
        stdout = io.StringIO()
        self.plugin.on_command(None, {"args": [None]}, stdout, stdout, None)
        self.assertEqual(self.plugin.on_help(), stdout.getvalue().strip())
