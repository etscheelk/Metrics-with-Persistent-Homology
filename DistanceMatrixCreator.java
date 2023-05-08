package finalProject;

import java.util.Scanner;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.lang.Math;
import java.io.FileWriter;



public class DistanceMatrixCreator {
    
    final String srcDelim;
    final String filePath;
    final String fileName;
    final String pathOut;

    final String[] funcList = {"Reg", "Block", "Cheby", "Discrete"};

    int numberOfPoints;
    double[][] points;

    public DistanceMatrixCreator(String srcDelim, String filePath, String fileName, String pathOut) throws FileNotFoundException, IOException {
        this.srcDelim = srcDelim;
        this.filePath = filePath;
        this.fileName = fileName;
        this.pathOut = pathOut;

        File file = new File(filePath + fileName);
        Scanner scan = new Scanner(file);

        numberOfPoints = 0;
        int dimension = -1;
        String line = "dud";
        while (scan.hasNextLine()) {
            line = scan.nextLine();
            numberOfPoints++;
        }
        dimension = line.trim().split(srcDelim).length;
        System.out.println("Number of points: " + numberOfPoints);
        System.out.println("Dimension of points: " + dimension);
        scan.close();


        scan = new Scanner(file);
        points = new double[numberOfPoints][dimension];
        int lineNumber = 0;
        while (scan.hasNextLine()) {
            String[] elements = scan.nextLine().trim().split(srcDelim);

            for (int x = 0; x < dimension; x++) {
                points[lineNumber][x] = Double.parseDouble(elements[x]);
            }
            lineNumber++;
        }
        scan.close();

        for (String funcType : funcList) {
            fillFile(funcType);
        }
    }

    private void fillFile(String funcType) throws IOException {
        File fileOut = new File(pathOut + fileName.substring(0, fileName.length()-4) + "-" + funcType + ".csv");
        fileOut.createNewFile();
        FileWriter writer = new FileWriter(fileOut);
        for (int i = 0; i < numberOfPoints; i++) {
            double[] point1 = points[i];

            for (int j = 0; j < numberOfPoints; j++) {
                double[] point2 = points[j];
                double distance;


                // Regular Distance
                if (funcType.equals(funcList[0]))
                    distance = regDistance(point1, point2);

                // Block Distance
                else if (funcType.equals(funcList[1]))
                    distance = blockDistance(point1, point2);

                // Chebyshev Distance
                else if (funcType.equals(funcList[2]))
                    distance = chebyshevDistance(point1, point2);
                
                // Discrete Distance
                else
                    distance = discreteDistance(point1, point2);

                
                // Don't add a space at the end of the line 
                if ((j+1) % numberOfPoints == 0) {
                    writer.write(distance + "");
                } else {
                    writer.write(distance + ", ");
                }
            }

            // Don't add a blank empty line at the end
            if ((i+1) % numberOfPoints != 0) {
                writer.write("\n");
            }
        }

        writer.close();
    }
    
    static double regDistance(double[] point1, double[] point2) {

        int dimension = point1.length;

        double sum = 0;
        for (int i = 0; i < dimension; i++) {
            double diff = Math.abs(point1[i] - point2[i]);
            sum += Math.pow(diff, 2);
        }

        return Math.sqrt(sum);
    }

    static double blockDistance(double[] point1, double[] point2) {

        int dimension = point1.length;

        double sum = 0;
        for (int i = 0; i < dimension; i++) {
            sum += Math.abs(point1[i] - point2[i]);
        }

        return sum;
    }

    static double chebyshevDistance(double[] point1, double[] point2) {

        int dimension = point1.length;

        double max = -1;
        for (int i = 0; i < dimension; i++) {
            double diff = Math.abs(point1[i] - point2[i]);
            if (diff > max) {
                max = diff;
            }
        }

        return max;
    }

    static double discreteDistance(double[] point1, double[] point2) {

        if (point1.equals(point2)) {
            return 0;
        } else {
            return 1;
        }
    }
}

class Main {
    public static void main(String[] args) throws FileNotFoundException, IOException {

        // "LaTeX/2023-04-14 ETS HW9/data/points400_2.csv"
        DistanceMatrixCreator dmc = new DistanceMatrixCreator(",", "LaTeX/2023-04-14 ETS HW9/data/", "points400_2.csv", "finalProject/data/");
        dmc = new DistanceMatrixCreator(",", "LaTeX/2023-04-14 ETS HW9/data/", "points400_1.csv", "finalProject/data/");
        dmc = new DistanceMatrixCreator(",", "LaTeX/2023-04-14 ETS HW9/data/", "points6.csv", "finalProject/data/");
        dmc = new DistanceMatrixCreator(",", "LaTeX/2023-04-14 ETS HW9/data/", "points12.csv", "finalProject/data/");


    }

    
}