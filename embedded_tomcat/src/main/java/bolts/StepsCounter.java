package bolts;

import java.util.Map;
import java.util.HashMap;

public class StepsCounter {
	public Map<String, Integer> counterMap;
	public void execute(){
		counterMap = new HashMap<String,Integer>();
		counterMap.put("This",1);
		counterMap.put("is",2);
		counterMap.put("bolts",3);
	}
	public Map<String,Integer> getMap(){
		this.execute();
		return this.counterMap;
	}
}
