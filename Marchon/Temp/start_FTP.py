import Calvin_Klein_FTP as ck
import Ferragamo_Temp_FTP as fe
import Lacoste_Temp_FTP as lc
import Nike_Temp_FTP as nk
import Victoria_Beckham_Temp_FTP as vb
def marchon_templates_updater():
    try:
        print("Creating Calvin Klein Templates file...")
        ck.callAllFunctions()
        print("Calvin Klein Templates file created succesfully!")
    except Exception as e:
        print(f"Error during creation Calvin Klein templates file. {type(e).__name__}: {e}")
    try:
        print("Creating Ferragamo Templates file...")
        fe.callAllFunctions()
        print("Ferragamo Templates file created succesfully!")
    except Exception as e:
        print(f"Error during creation Ferragamo templates file. {type(e).__name__}: {e}")
    try:
        print("Creating Lacoste Templates file...")
        lc.callAllFunctions()
        print("Lacoste file created succesfully!")
    except Exception as e:
        print(f"Error during creation Lacoste templates file. {type(e).__name__}: {e}")
    try:
        print("Creating Nike Templates file...")
        nk.callAllFunctions()
        print("Nike file created succesfully!")
    except Exception as e:
        print(f"Error during creation Nike templates file. {type(e).__name__}: {e}")
    try:
        print("Creating Victoria Beckham Templates file...")
        vb.callAllFunctions()
        print("Victoria Beckham file created succesfully!")
    except Exception as e:
        print(f"Error during creation Victoria Beckham templates file. {type(e).__name__}: {e}")

if __name__ == "__main__":
    marchon_templates_updater()
    print("All templates brands file are saved succesfully into \"Temp\" directory.")
