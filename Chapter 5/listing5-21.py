from database.garage_v1 import MyGarage
VENDOR_COLS_CREATE = ['Name', 'URL', 'Sources']
VENDOR_COLS = []
VENDOR_COLS.extend(VENDOR_COLS_CREATE)
VENDOR_COLS.insert(0, 'Id') # Add the Id to the list
class Vendor(object):
    def __init__(self, mygarage):
        self.mygarage = mygarage
        self.schema = mygarage.get_db()
        self.tbl = self.schema.get_table('vendor')
    
    
    def create(self, vendor_data):
        vendor_name = vendor_data.get("Name", None)
        link = vendor_data.get("URL", None)
        sources = vendor_data.get("Sources", None)
        assert vendor_name, "You must supply a name for the vendor."
        try:
            self.tbl.insert(VENDOR_COLS_CREATE).values(vendor_name, link, sources).execute()
        except Exception as err:
            print("ERROR: Cannot add vendor: {0}".format(err))
            return (False, err)
        return (True, None)
    
    
    def read(self, vendor_id=None):
        if not vendor_id:
            # return all vendors
            sql_res = self.tbl.select(VENDOR_COLS).order_by("Name").execute()
        else:
            # return specific vendor
            sql_res = self.tbl.select(VENDOR_COLS).where(
                "Id = '{0}'".format(vendor_id)).execute()
        return self.mygarage.make_rows(sql_res)
    


mygarage = MyGarage(mysqlx)
mygarage.connect('root', 'SECRET', 'localhost', 33060)
vendor = Vendor(mygarage)
vendor_data = {
    "Name": "ACME Bolt Company",
    "URL": "www.acme.org",
    "Sources": "looney toons"
}
    
    
vendor.create(vendor_data)
last_id = mygarage.get_last_insert_id()[0]
print("Last insert id = {0}".format(last_id))
rows = vendor.read(last_id)
print("{0}".format(", ".join(rows[0])))
rows = vendor.read()
print(rows[:5])

