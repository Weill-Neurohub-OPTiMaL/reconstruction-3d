import java.io.*;
import java.util.*;

public class RenameInterleave {

    public static final int NUM_CAMS = 3;
    public static final int NUM_WIDTH = 6;
    public static final String SLASH = "/";

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
            
            String num = padWithZeros(i, NUM_WIDTH);
            String firstFilename = "cam0_" + num + ".jpg";
            String secondFilename = "cam4_" + num + ".jpg";
            String thirdFilename = "cam8_" + num + ".jpg";


            String ctr1 = padWithZeros(ctr, NUM_WIDTH);
            File file_1 = new File(dir_name + SLASH + firstFilename);
            File dest_1 = new File(dir_name + SLASH + "renamed_" + ctr1 + ".jpg");

            ctr++;

            String ctr2 = padWithZeros(ctr, NUM_WIDTH);
            File file_2 = new File(dir_name + SLASH + secondFilename);
            File dest_2 = new File(dir_name + SLASH + "renamed_" + ctr2 + ".jpg");

            ctr++;

            String ctr3 = padWithZeros(ctr, NUM_WIDTH);
            File file_3 = new File(dir_name + SLASH + thirdFilename);
            File dest_3 = new File(dir_name + SLASH + "renamed_" + ctr3 + ".jpg");

            ctr++;

            boolean flag_1 = file_1.renameTo(dest_1);
            boolean flag_2 = file_2.renameTo(dest_2);
            boolean flag_3 = file_3.renameTo(dest_3);

            if (flag_1 == true && flag_2 == true && flag_3 == true) {
                System.out.println("Files successfully renamed");
                System.out.println("Reading from " + firstFilename);
                System.out.println("Reading from " + secondFilename);
                System.out.println("Reading from " + thirdFilename);
                System.out.println("Renamed to " + "renamed_" + ctr1 + ".png");
                System.out.println("Renamed to " + "renamed_" + ctr2 + ".png");
                System.out.println("Renamed to " + "renamed_" + ctr3 + ".png");
            } else {
                System.out.println("Operation Failed");
            }
        }
    }

    public static String padWithZeros(int num, int num_zeros) {
        String num_str = String.valueOf(num);
        while (num_str.length() < num_zeros) {
            num_str = '0' + num_str;
        }
        return num_str;
    }
}
