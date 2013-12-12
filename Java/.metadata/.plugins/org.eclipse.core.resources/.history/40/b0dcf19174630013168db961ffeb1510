import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.*;

public class Downsample 
{	
	public static void main(String[] args) throws IOException
	{
		String inputFileName = "movementDataProcessed.csv";
		String outputFileName = "movementDataDownsampled.csv";

		HashMap<String, HashMap<String, Integer>> movement = new HashMap<String, HashMap<String, Integer>>();
		BufferedReader br = new BufferedReader(new FileReader(inputFileName));
		String line;
		while ((line = br.readLine()) != null) 
		{
			String[] lineSplit = line.split(",");
			if (!movement.containsKey(lineSplit[0]))
				movement.put(lineSplit[0], new HashMap<String, Integer>());
			movement.get(lineSplit[0]).put(lineSplit[1], Integer.parseInt(lineSplit[2]));
		}
		br.close();
		
		ArrayList<String[]> list = new ArrayList<String[]>();
		for (Map.Entry<String, HashMap<String, Integer>> entry1 : movement.entrySet()) 
		{
		    String key1 = entry1.getKey();
		    HashMap<String, Integer> value1 = entry1.getValue();
		    for (Map.Entry<String, Integer> entry2 : value1.entrySet()) 
			{
			    String key2 = entry2.getKey();
			    Integer value2 = entry2.getValue();
			    for (int i = 0; i < value2; i++)
			    {
			    	String[] element = {key1, key2};
			    	list.add(element);
			    }
			    movement.get(key1).put(key2, 0);
			}
		}
				
		Collections.shuffle(list);
				
		int n = (int) (list.size() * 0.2);
				
		for (int i = 0; i < n; i++)
		{
			String[] element = list.get(i);
			int previous = movement.get(element[0]).get(element[1]);
			movement.get(element[0]).put(element[1], previous + 1);
		}		
		StringBuilder output = new StringBuilder();
		for (Map.Entry<String, HashMap<String, Integer>> entry1 : movement.entrySet()) 
		{
		    String key1 = entry1.getKey();
		    HashMap<String, Integer> value1 = entry1.getValue();
		    for (Map.Entry<String, Integer> entry2 : value1.entrySet()) 
			{
			    String key2 = entry2.getKey();
			    Integer value2 = entry2.getValue();
			    if (value2 >= 20)
			    {
			    	output.append(key1 + "," + key2 + "," + value2 + "\n");
			    }
			}
		}
		
		BufferedWriter writer = new BufferedWriter(new FileWriter(outputFileName));
		writer.write(output.toString());
		writer.close();
	}
}
