import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;

public class OutputFlux 
{
	public static void main(String args[]) throws IOException 
	{
		String divisionsFileName = Globals.projectDirectory + 
				"usData/usDivisionsCommuters.csv";
		
		Division.loadDivisions(divisionsFileName);

		ArrayList<String> keys = new ArrayList<String>();
		keys.addAll(Division.divisions.keySet());
		Collections.sort(keys);
		
		int index = Integer.parseInt(args[0]);
		int count = Integer.parseInt(args[1]);
		
		for (int i = index; i < index + count; i++)
		{
			new Flux(keys.get(i));
		}
	}
}