package servlet;

import bolts.StepsCounter;

import java.io.IOException;
import java.util.Map;
import java.util.HashMap;
import java.util.Set;

import javax.servlet.ServletException;
import javax.servlet.ServletOutputStream;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet(
	name = "MyServlet",
	urlPatterns = {"/hello"}
	)
public class HelloServlet extends HttpServlet {
	
	@Override
	protected void doGet(HttpServletRequest req, HttpServletResponse resp)
		throws ServletException, IOException {
		ServletOutputStream out = resp.getOutputStream();
		StepsCounter sc = new StepsCounter();
		Map<String,Integer> cMap = sc.getMap();
		if(cMap==null)
			cMap = new HashMap<String,Integer>();
		cMap.put("end",99);
		StringBuilder ss = new StringBuilder();
		Set<Map.Entry<String,Integer>> curSet = cMap.entrySet();
		for(Map.Entry<String,Integer> entry:curSet){
			ss.append(" "+entry.getKey()).append(" : "+entry.getValue());
		}
		//out.write("hello embedded tomcat".getBytes());
		out.write(ss.toString().getBytes());
		out.flush();
		out.close();
	}
	
}

