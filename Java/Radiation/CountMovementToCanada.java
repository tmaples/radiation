import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;

public class CountMovementToCanada 
{
	static String inputFileName = "movementDataProcessed.csv";
	static String outputFileName = "movementToCanadaData.csv";

	public static void main(String[] args) throws IOException
	{
		BufferedReader br = new BufferedReader(new FileReader(inputFileName));
		String line;
		String[] data;
		
		StringBuilder output = new StringBuilder();
		
		while ((line = br.readLine()) != null) 
		{
			data = line.split(",");
			if (data[1].equals("301"))
				output.append(data[0] + "," + data[2] + "\n");
		}
		
		br.close();
		
		BufferedWriter writer = new BufferedWriter(new FileWriter(outputFileName));
		writer.write(output.toString());
		writer.close();
	}
}
