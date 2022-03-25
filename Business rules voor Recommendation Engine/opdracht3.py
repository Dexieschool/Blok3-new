import pymongo
import psycopg2

#probeer de connectie te maken met de sql database
try:
    conn = psycopg2.connect("dbname=Opdracht2AI user=postgres host=localhost password=<veranderdit>")
except:
    print( "I am unable to connect to the database")

#maak de cursor aan
cur = conn.cursor()

# global variables and settings

# aantal reconmendations
lengte = 4

# met deze setting kies je of je wilt sorteren uit prev_recommended of viewed_before
# je kan een index kiezen voor welke eigenschap je wilt
profieleigenschappen = ['prev_recommended','viewed_before']
setting1 = profieleigenschappen[0]

# global productid en profielid deze kan je veranderen
productid = '29244'
profielid = '5a3a0a51a825610001bc0a13'



# return alle data van het referentie product
def firstproductData(id):
    selecterstatement = "select * from product where product_id = %s"
    cur.execute(selecterstatement, (id,))
    productdata = cur.fetchall()
    return productdata

# hiermee kan je filter regel custimize op een kolom. je kunt bijvoorbeeld alle producten pakken die dezelfde brand hebben
def customproductreco():
    productdata = firstproductData(productid)
    customregel = "select * from product where {} = %s".format(setting1)
    cur.execute(customregel, (productdata[0],))
    customdata = cur.fetchall()
    count = 0
    customreco = []
    for i in customdata:
        customreco.append(i)
        if count == 4:
            break
    return customreco


# de eerste recommendation regel content filtering
def productreco():
    productdata = firstproductData(productid)
    sum1 = productdata[0][5] - 1000
    sum2 = productdata[0][5] + 1000
    # de sorteer regel
    newstatement ="select * from product where selling_price BETWEEN %s AND %s AND category = %s AND sub_category = %s AND sub_sub_category = %s AND brand = %s"
    sort = [sum1,sum2,productdata[0][7],productdata[0][8],productdata[0][9],productdata[0][1]]
    cur.execute(newstatement,(sort))
    row = cur.fetchall()
    count = 0
    productrecommendationlist = []
    for i in row:
        count += 1
        productrecommendationlist.append(i[0])
        if count == 4:
            break
    return productrecommendationlist



# dit pakt data uit de prev_recomended tabel met de profiel_id waar de segment hetzelfde is
def viewedbefore(id):
    viewedbeforequery = "select * from {} where profiel_id = %s".format(setting1)
    cur.execute(viewedbeforequery,(id,))
    viewedbeforedata = cur.fetchone()
    return viewedbeforedata


# haalt de data van het gekozen profiel op
def firstprofielData(id):
    profielselect = "select * from profiels where profiel_id = %s"
    cur.execute(profielselect,(id,))
    firstprofieldata = cur.fetchall()
    return firstprofieldata

# deze functie maakt een recomendation op basis van welke segment het id is. bijv(bouncer,buyer etc..)
# dan pakt de functie een profiel id die het zelfde segment heeft en kijkt wat de profielid zijn prev_recomended is.
# dit is de collaborative filter regel
def profielsreccomandation(id):

    profielselect = "select profiel_id from profiels where segment = %s"
    # gebruikt de firstprofieldata functie om data op te halen
    firstprofielsegment = firstprofielData(id)[0][1]
    cur.execute(profielselect,(firstprofielsegment,))
    similar = cur.fetchall()
    similarproducts = []
    count = 0
    for i in similar:
        temp = viewedbefore(i)
        if temp == None:
            continue
        similarproducts.append(temp[1])
        count += 1
        if count == 4:
            break
    return similarproducts

# call statements
print(productreco())
print(profielsreccomandation(profielid))