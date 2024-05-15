from gpiozero import Buzzer
from gpiozero import Button
import RPi.GPIO as GPIO
from time import sleep
import os

# funksjoner
import kamera_ta_bilde
import ansikt_gjenkjenn
import filbehandling
import opprette_db_tabell
import send_epost

# sett opp buzzer og knapp
buzzer = Buzzer(17)
button = Button(23)

# sett opp GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(21,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)

# sett opp grønn og rød LED
LED_PIN_GRN = 21
LED_PIN_RD = 13

# hovedløkke som styrer programmet. fortsetter frem til
# det avsluttes av bruker
def app():
    try:
        while True:
            # venter på knappetrykk fra bruker.
            # skru på buzzer og gr/rø LED
            print("Venter på knappetrykk...")
            button.wait_for_press()
            buzzer.on()
            sleep(0.4)
            buzzer.off()
            sleep(1)
            
            print("Knapp trykket! Skru på LED")
            GPIO.output(21, GPIO.HIGH)
            GPIO.output(13, GPIO.HIGH)
            sleep(3)

            # ta bilde med PiCamera
            kamera_ta_bilde.ta_bilde()

            print("Skru av LED")
            GPIO.output(21, GPIO.LOW)
            GPIO.output(13, GPIO.LOW)
            print("---------------------------------------------------------")
            print("")
            
            # face recognition.
            # gjenkjent = ansikt_gjenkjenn.ansikt_gjenkjenn()
            print("Begynner ansiktsgjenkjenning...")
            gjenkjent, person_id = ansikt_gjenkjenn.ansikt_gjenkjenn()

            # person i bilde blir gjenkjent. slett bilde
            # og lås opp dør (skru på grønn led) samt
            # skru på buzzer en gang
            if gjenkjent == True:
                print(f"Velkommen {person_id}")
                print("Skrur på grønn LED")
                filbehandling.slett_bilde()

                buzzer.on()
                sleep(0.4)
                buzzer.off()
                
                GPIO.output(21, GPIO.HIGH)
                sleep(2)
                GPIO.output(21, GPIO.LOW)
                
            # person i bilde blir ikke gjenkjent. lagre bilde i mappe <bilder>,
            # skru på rød led, og sett på buzzer to ganger
            # Send e-postvarsel
            else:
                print("Person ikke gjenkjent. Skru på rød LED")
                filnavn = filbehandling.lagre_bilde()
                
                send_epost.send_epost(filnavn)
                print("Varsel sendt på e-post!")

                buzzer.on()
                sleep(0.4)
                buzzer.off()
                buzzer.on()
                sleep(0.4)
                buzzer.off()
                
                GPIO.output(13, GPIO.HIGH)
                sleep(2)
                GPIO.output(13, GPIO.LOW)

            print("---------------------------------------------------------")
            print("")
            
    except KeyboardInterrupt:
        print("Program avsluttet")
        

def main():
    # oppstart av program med logo
    logo()
    print("")
    print("/-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-\\")
    print("| FRODOLARSSEN v.0.9 -----------------------------------|")
    print("| Facial RecOgnition DOor Lock -------------------------|")
    print("|-- And Reactive Surveillance System -------------------|")
    print("|---- with Email Notification --------------------------|")
    print("\.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-./")
    print("")
    print("Velkommen! Starter opp...")
    print("")

    # sjekk om mappe "bilder" finnes. finnes den ikke,
    # opprett mappen, så fortsett programoppstart
    print("Finner ressurser...")
    if os.path.exists("bilder"):
        print("Mappe 'bilder' funnet!")
    else:
        print("Mappe 'bilder' ikke funnet!")
        os.mkdir("bilder")
        print("Opprettet mappe 'bilder'!")
        
    # sjekk om db finnes. finnes den ikke, opprett ny fil,
    # så fortsett programoppstart
    if os.path.exists("bilder.db"):
        print("Database 'bilder.db' funnet!")
    else:
        print("Database 'bilder.db' ikke funnet!")
        print("Oppretter ny database...")
        opprette_db_tabell.opprett()
        print("Ny database opprettet!")

    print("---------------------------------------------------------")
    print("")
    # start opp hovedløkke
    app()

# printer ascii logo
def logo():                                                                       
    print("                @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                                    ")
    print("               @@................................@@                                   ")
    print("              @@.:------------------------------..@@%                                 ")
    print("             @@..-------------------------------::+@@@@@@@@@@@@@@@@+                  ")
    print("            @@.-:--------------------------------:.................@@                 ")
    print("           @@:-:-------------------------------------------------:.*@@                ")
    print("          @%+.:---------------------------------------------------:.@%@               ")
    print("         @@%        .   .:.     ..      ::.     .------------------..@%               ")
    print("        @%#: @@@@@.@@@@@#  @@@@@  @@@@@@  *@@@@@ :------------------..@%              ")
    print("       @%@.. @#%   @#+-%@ @%@ @%@ @#@ @%@ @## %@*.-------------------..@@             ")
    print("      *%@..- @#%.= @#*##@ @#@ @#@ @#@ @#@ @## %%# -------=-=----------..@@            ")
    print("      #@..-- @#%@@ @##%#@ @#@ @#@ @#@ @#@ @## %%# ---------------------..@@           ")
    print("     @@..--- @#@   @#*.%@ @#@ @#@ @#@ @#@.@## %@#.----------------------..@@          ")
    print("    %@..---- @@@ :-@@@#@@ %@@@@@@ @@@@@@@ @@@@@@.:-----------------------.=@@         ")
    print("   #@..-----.. ..-..      .       .             ::.   .:.        ..  .---:.+*         ")
    print("  #@.:--------------.@@@*.- @@@@  @@@%@.   @@@@   #@@@  :@@@@@*@@ -@@ ---..@@         ")
    print(" %@..--------------- #%@-.: @##%@ @#%*@@@ @%##@@ @%% @@@.@#%@%-%%@ @@ --:.@#          ")
    print(" %@..--------------- #%@-..+%#*%@ @#%.#%@ @%%    @%%.   .@#*  =%#% %@ --.:#@          ")
    print("  %@..-------------- #%@-. @## #@ @#%%%%   %%@@@  #%@@@  @#@@-+%#%%#@ -..@@           ")
    print("   %@..------------- #%%   @#%%%@ %#% %%@ @%+*#@.@%@ @%@.@#*  -%%#%#@ ..@@            ")
    print("    %@..------------ #%#%@ @#%.%%*##@ %#@ @%# %@:@%@ @%@ @#%@@:%@ @#@ .@%             ")
    print("     %%..-----------.@@@@@-@@@ @@@@@@:@@@  @@@@.  =@@@* :@@@@@+@@ @@@ +@@             ")
    print("     @%@.:----------:.     .             ..    .-:.   ...        ..  *@@              ")
    print("      @#=.:--------------------------------------------------------..@@               ")
    print("       @@=.:-------------------------------------------------------.@%                ")
    print("        @@..-------------------------------------------:::::::::::.=@@                ")
    print("         @@..---------------------------------------...............@@                 ")
    print("          @@..-------------------------------------..%@@@@-------                     ")
    print("           @@..-----------------------------------:.%%@                               ")
    print("            @@..----------------------------------..@@                                ")
    print("             @@..--------------------------------..@@                                 ")
    print("              @@..------------------------------..@@                                  ")
    print("               @@................................@@                                   ")
    print("                @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                                    ")
                                                                
                                                                                
# start program                                                                   
main()
        
