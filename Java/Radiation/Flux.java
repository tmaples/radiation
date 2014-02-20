import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;

class Flux implements Runnable
{
	Thread t;
	String uid;
	String fileName;

	Flux(String uid) 
	{
		this.t = new Thread(this, uid);
		this.uid = uid;
		this.fileName = Globals.projectDirectory + "fluxCanadaToUsAndCanada/flux" + uid + ".csv";
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

			StringBuilder output = new StringBuilder("uid,movement");

			for (String dest : Division.divisions.keySet())
			{
				if (uid.equals(dest))
					continue;
				int flux = Division.flux(Division.divisions.get(uid), Division.divisions.get(dest));
				if (flux > 0)
					output.append("\n" + dest + "," + flux);
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