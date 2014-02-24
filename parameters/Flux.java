import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;

class Flux implements Runnable
{
	Thread t;
	String uid;
	String fileName;

	Flux(String uid) 
	{
		this.t = new Thread(this, uid);
		this.uid = uid;
		this.fileName = "parameters/parameters" + uid + ".csv";
		t.start();
	}

	public void run() 
	{
		File file = new File(fileName);
		if(file.exists())
			return;

		BufferedWriter writer = null;
		try 
		{
			writer = new BufferedWriter(new FileWriter(fileName));

			StringBuilder output = new StringBuilder("uid,population,distance,radiusPopulation");

			ArrayList<String> dests = new ArrayList<String>();
			dests.addAll(Division.divisions.keySet());
			Collections.sort(dests);

			for (String dest : dests)
			{
				if (uid.equals(dest))
					continue;
				double distance = Division.distance(Division.divisions.get(uid), Division.divisions.get(dest));
				int radius = Division.radiusPopulation(Division.divisions.get(uid), Division.divisions.get(dest));
				int pop = Division.divisions.get(dest).population;
				output.append("\n" + dest + "," + pop + "," + distance + "," + radius);
			}

			writer.write(output.toString());
			writer.close();
		} 
		catch (IOException e) 
		{
			e.printStackTrace();
		}
		
		System.out.println(Division.divisions.get(uid).name + " Complete.");
	}
}