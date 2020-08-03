from flask import Flask, request, render_template
app = Flask(__name__)
from modules.base64_to_list import base_converter
from modules.db_connector import connection
import os
import jinja2

template_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_env = jinja2.Environment(loader= jinja2.FileSystemLoader(template_dir),autoescape=True)



@app.route('/v1/unsubscribe/')
def application():
    if len(request.args) == 2:
        #GETTING THE PARAMETERS OF THE QUERY
        params = dict(request.args)
        fields = tuple(params.keys())


        #validating the received fields with the required fields
        counter = 0
        required_fields = ['email','vin']
        for f in fields:
            if f not in required_fields:
                counter += 1

        #making sure that the fields are allowed to be inserted
        if counter != 0:
            #RETURN AND BAD PARAMENTERS TEMPLATE IN CASE THE FIELDS ARE NOT ALLOWED
            return render_template('bad_params.html')

        #RECEIVING THE DECODED DICT FROM THE LIBRARY
        values = base_converter(params)
        
        #VALIDATING THAT THE VALUES ARE ALLOWED TO BE INSERTED AND ARE ENCRIPTED
        if values == None:
            return render_template('not_allowed_values.html')

        #INTERACTING WITH THE DATABASE
        try:
            #CONNECTION WITH THE DATABASE ENGINE
            mdb = connection()

            #VALIDATING THAT THE VIN AND EMAIL ARE NOT ALREADY INSERTED IN THE TABLE AND IF SUCH RETURNING DUPLICATED ENTRY TEMPLATE
            cursor = mdb.cursor()
            # print('SELECT * FROM unsubscribe where email = "{email}" and vin = "{vin}";'.format(**values))
            cursor.execute(
                'SELECT * FROM unsubscribe where email = "{email}" and vin = "{vin}";'.format(**values)
            )
            if len(cursor.fetchall()) > 0:
                return render_template('duplicated_entry.html')

            #INSERTING THE VALUES IN THE TABLE AND RETURNING THE SUCCESS OPERATION TEMPLATE
            field = str(tuple(values.keys())).replace("'","")
            values = list(values.values())
            print(
                'INSERT INTO unsubscribe {fields} VALUES (%s,%s)'.format(
                    fields = field
                )
            )
            cursor.execute(
                'INSERT INTO unsubscribe {fields} VALUES (%s,%s)'.format(
                    fields = field
                ),
                values
            )
            return render_template('unsubscribed.html')

        except EnvironmentError as err:
            print(err)

        finally:
            #ALWAYS MAKE SURE TO CLOSE THE CONNECTION WITH THE DATABASE
            mdb.close()
        
    else:
        #IF THERE IS NO QUERY THEN RETURN HOME PAGE
        return render_template('home.html')

if __name__ == "__main__":
    app.run()