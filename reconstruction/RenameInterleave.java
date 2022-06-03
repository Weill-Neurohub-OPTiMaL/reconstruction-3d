import java.io.*;
import java.util.*;

public class RenameInterleave {

    public static final int NUM_CAMS = 3;

    public static void main(String[] args) throws IOException {

        // String dir_name = "C:\\Users\\User\\CSE600\\wasabi_videos\\3-11-22_videos\\video_tapping_images_2m_interleaved_naming";
        String dir_name = args[0];
        File dir = new File(dir_name);

        // Get list of all the files in form of String Array
        String[] fileNamesUnsorted = dir.list();

        String[] fileNames = new String[fileNamesUnsorted.length];
        for (int i = 0 ; i < fileNamesUnsorted.length ; i++) {
            fileNames[i] = fileNamesUnsorted[i];
        }

        // Loop for reading the contents of all the files in the directory.
        int ctr = 1;
        for (int i = 1 ; i <= fileNames.length / NUM_CAMS ; i++) {

            String firstFilename = "cam0 (" + i + ").png";
            String secondFilename = "cam4 (" + i + ").png";
            String thirdFilename = "cam8 (" + i + ").png";

            File file_1 = new File(dir_name + "\\" + firstFilename);
            File dest_1 = new File(dir_name + "\\" + "renamed_" + ctr + ".png");

            ctr++;

            File file_2 = new File(dir_name + "\\" + secondFilename);
            File dest_2 = new File(dir_name + "\\" + "renamed_" + ctr + ".png");

            ctr++;

            File file_3 = new File(dir_name + "\\" + thirdFilename);
            File dest_3 = new File(dir_name + "\\" + "renamed_" + ctr + ".png");

            ctr++;

            boolean flag_1 = file_1.renameTo(dest_1);
            boolean flag_2 = file_2.renameTo(dest_2);
            boolean flag_3 = file_3.renameTo(dest_3);

            if (flag_1 == true && flag_2 == true && flag_3 == true) {
                System.out.println("Files successfully renamed");
                System.out.println("Reading from " + firstFilename);
                System.out.println("Reading from " + secondFilename);
                System.out.println("Reading from " + thirdFilename);
                System.out.println("Renamed to " + "renamed_" + (ctr-3) + ".png");
                System.out.println("Renamed to " + "renamed_" + (ctr-2) + ".png");
                System.out.println("Renamed to " + "renamed_" + (ctr-1) + ".png");
            } else {
                System.out.println("Operation Failed");
            }
        }
    }
}