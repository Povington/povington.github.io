package authentication.page;
/**
 * Simple authentication page that accepts username and password. Creates MD5 hash of password and scans .txt files.
 * @author Povington
 */

import java.util.Scanner;
import java.io.FileInputStream;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

public class AuthenticationPage {

    public static void main(String[] args) throws Exception {

        Scanner scnr = new Scanner(System.in);
        Scanner inFS;
        String userName, userPass, logout, passHash = null, user = null;
        int userAttempts = 0;
        boolean inputDone = false;

        /* initialize files. FIXME implement try block and catch fileNotFound */
        FileInputStream zookeeper = new FileInputStream("zookeeper.txt");
        FileInputStream admin = new FileInputStream("admin.txt");
        FileInputStream veterinarian = new FileInputStream("vet.txt");
        FileInputStream credentialsFile = new FileInputStream("credentialsFile.txt");

        /* Main while loop. Iterates until input is done or user login attempts exceed set value. */
        while (!inputDone) if (userAttempts > 3) {
            System.out.println("Too many attempts used. Exiting Program");
            break;
        } else {
            System.out.println("Enter username (Type q to exit): ");
            userName = scnr.nextLine();
            if (userName.equals("q")) {
                System.out.println("Exiting program. Goodbye.");
                break;
            } else {
                System.out.println("Enter password: ");
                userPass = scnr.nextLine();
                passHash = hashPassword(userPass);
            }
            inFS = new Scanner(credentialsFile);

            /* Search entire .txt file for username. Pull the line the username is found. Break when found. */
            /* FIXME if there isn't a set null value at the end of the file this saves the last read line as user.
            Bug can cause incorrect password attempts. */
            while (inFS.hasNextLine()) {
                user = inFS.nextLine();
                if (user.contains(userName)) {
                    break;
                }
            }

            /* Verifies tha username and password hash match the user file pulled. Increments user attempts by 1 for
            failed attempt. */
            if ((user.contains(userName) && (user.contains(passHash)))) {
                //FIXME if statement iterates three times. Set up method to make this more efficient.
                if(user.contains("zookeeper")){
                    inFS = new Scanner(zookeeper);
                    while (inFS.hasNextLine()) {
                        String line = inFS.nextLine();
                        System.out.println(line);
                    }
                }
                else if (user.contains("admin")) {
                    inFS = new Scanner(admin);
                    while (inFS.hasNextLine()) {
                        String line = inFS.nextLine();
                        System.out.println(line);
                    }
                }
                else if (user.contains("veterinarian")){
                    inFS = new Scanner(veterinarian);
                    while (inFS.hasNextLine()) {
                        String line = inFS.nextLine();
                        System.out.println(line);
                    }
                }

                System.out.println("Enter q to exit");
                logout = scnr.nextLine();

                if (logout.equals("q")) {
                    System.out.println("Exiting program.");
                    inputDone = true;
                }
                /* Quits program for unexpected input. Other inputs to be added. */
                else{
                    System.out.println("Error: Unrecognized command. Exiting Program");
                    inputDone = true;
                }
            }
            else {
                userAttempts++;
                System.out.println("Error: Username or Password incorrect");
            }
        }
    }

    //Method used for hashing passwords. Creates MD5 hash and returns value.
    public static String hashPassword(String original) {

        try {

            MessageDigest md = MessageDigest.getInstance("MD5");
            md.update(original.getBytes());
            byte[] digest = md.digest();
            StringBuffer sb = new StringBuffer();
            for (byte b : digest) {
                sb.append(String.format("%02x", b & 0xff));
            }
            return sb.toString();

        } catch (NoSuchAlgorithmException e) {
            e.printStackTrace();
        }
        return null;
    }
}
