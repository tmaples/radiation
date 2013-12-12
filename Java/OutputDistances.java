import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.HashMap;

public class OutputDistances 
{
	private static HashMap<String, HashMap<String, Integer>> movement;
	
	private static void loadMovement(String fileName) throws NumberFormatException, IOException
	{
		movement = new HashMap<String, HashMap<String, Integer>>();
		for (String uid : Division.divisions.keySet())
		{
			movement.put(uid, new HashMap<String, Integer>());
		}
		
		BufferedReader br = new BufferedReader(new FileReader(fileName));
		String line;
		String[] data;
		
		while ((line = br.readLine()) != null) 
		{
			data = line.split(",");
			movement.get(data[0]).put(data[1], Integer.parseInt(data[2]));
		}
		
		br.close();
	}
	
	private static void run(String movementFileName) throws NumberFormatException, IOException
	{
		loadMovement(movementFileName);
		
		StringBuilder output = new StringBuilder();
		
		int[] x = new int[1000];
		for (int i = 0; i < x.length; i++)
			x[i] = (i+1)*10;
		int[] y = new int[1000];
		
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
		
		BufferedWriter writer = new BufferedWriter(new FileWriter(movementFileName + "XY.csv"));
		writer.write(output.toString());
		writer.close();
	}
	
	public static void main(String args[]) throws IOException
	{
		String movementFileName = "movementDataDownsampled";
		Division.loadDivisions("usaDivisions2000");
		for (int i = 1; i <= 10; i++)
		{
			run(movementFileName + i);
		}
	}
}
