package com.ai.aws.iam.repository;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class IAMRepository {
	private Connection conn;

	public IAMRepository() throws Exception {
		Class.forName("com.mysql.cj.jdbc.Driver");
		conn = DriverManager.getConnection("jdbc:mysql://localhost:3306/ai_aws_iam?useSSL=false", "root", "admin");
	}

	public List<Map<String, String>> getAllUsersWithAI() throws Exception {
		List<Map<String, String>> users = new ArrayList<>();
		String sql = "SELECT username, arn, create_date, ai_analysis FROM iam_users";
		Statement stmt = conn.createStatement();
		ResultSet rs = stmt.executeQuery(sql);

		while (rs.next()) {
			Map<String, String> user = new HashMap<>();
			user.put("Username", rs.getString("username"));
			user.put("ARN", rs.getString("arn"));
			user.put("Created", rs.getString("create_date"));
			user.put("AI", rs.getString("ai_analysis"));
			users.add(user);
		}
		return users;
	}
}
