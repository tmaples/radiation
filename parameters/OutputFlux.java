import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;

public class OutputFlux 
{
	public static void main(String args[]) throws IOException 
	{
		String divisionsFileName = "continentDivisions.csv";
		
		Division.loadDivisions(divisionsFileName);

		ArrayList<String> keys = new ArrayList<String>();
		
		for (String key : Division.divisions.keySet())
		{
			if (key.charAt(0) == 'U')
				keys.add(key);
		}
		
		Collections.sort(keys);
		
		int index = Integer.parseInt(args[0]);
		int count = Integer.parseInt(args[1]);
		
		for (int i = index; i < index + count; i++)
		{
			if (i < keys.size())
				new Flux(keys.get(i));
		}
	}
}