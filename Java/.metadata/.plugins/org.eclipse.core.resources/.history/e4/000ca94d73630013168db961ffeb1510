import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.HashMap;

public class DistanceToWork 
{
	static String movementFileName = "movementDataDownsampled.csv";
	static String divisionFileName = "usaDivisions2000.csv";
	static String outputFileName = "distanceToWork.csv";

	static int binSize = 10;
	static int maxDistance = 10000;

	static HashMap<String, HashMap<String, Integer>> movement;
	
	static void loadMovement() throws NumberFormatException, IOException
	{
		movement = new HashMap<String, HashMap<String, Integer>>();
		
		for (String uid : Division.divisions.keySet())
		{
			movement.put(uid, new HashMap<String, Integer>());
		}
		
		BufferedReader br = new BufferedReader(new FileReader(movementFileName));
		String line;
		String[] data;
		
		while ((line = br.readLine()) != null) 
		{
			data = line.split(",");
			movement.get(data[0]).put(data[1], Integer.parseInt(data[2]));
		}
		
		br.close();
	}
	
	static void outputDistanceToWork() throws NumberFormatException, IOException
	{
		StringBuilder output = new StringBuilder();
		
		int[] x = new int[maxDistance / binSize];
		for (int i = 1; i < x.length + 1; i++)
			x[i] = i * binSize;
		int[] y = new int[maxDistance / binSize];
		
		for (Division divisionA : Division.divisions.values())
		{
			for (Division divisionB : Division.divisions.values())
			{
				if (Division.equal(divisionA, divisionB))
					continue;
				if (movement.get(divisionA.uid).containsKey(divisionB.uid))
				{
					Integer number = movement.get(divisionA.uid).get(divisionB.uid);
					Integer bin = (int) (Division.distance(divisionA, divisionB) / 10);
					y[bin] += number;
				}	
			}
		}
		
		for (int i = 0; i < x.length; i++)
		{
			output.append(x[i] + "," + y[i] + "\n");
		}
		
		BufferedWriter writer = new BufferedWriter(new FileWriter(outputFileName));
		writer.write(output.toString());
		writer.close();
	}
	
	public static void main(String args[]) throws IOException
	{
		Division.loadDivisions(divisionFileName);
		loadMovement();
		outputDistanceToWork();
	}
}