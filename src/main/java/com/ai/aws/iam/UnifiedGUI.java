package com.ai.aws.iam;

import java.awt.BorderLayout;
import java.util.List;
import java.util.Map;

import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JOptionPane;
import javax.swing.JScrollPane;
import javax.swing.JTable;
import javax.swing.SwingUtilities;
import javax.swing.table.DefaultTableModel;

import com.ai.aws.iam.repository.IAMRepository;

public class UnifiedGUI extends JFrame {
	private JTable table;

	public UnifiedGUI() {
		setTitle("AWS IAM Users + AI Analysis");
		setSize(1000, 600);
		setDefaultCloseOperation(EXIT_ON_CLOSE);
		setLayout(new BorderLayout());

		String[] columns = { "Username", "ARN", "Created", "AI Analysis" };
		table = new JTable(new DefaultTableModel(columns, 0));
		add(new JScrollPane(table), BorderLayout.CENTER);

		JButton refreshBtn = new JButton("Load IAM + AI");
		refreshBtn.addActionListener(e -> loadUsers());
		add(refreshBtn, BorderLayout.SOUTH);

		setVisible(true);
	}

	private void loadUsers() {
		try {
			IAMRepository repo = new IAMRepository();
			List<Map<String, String>> users = repo.getAllUsersWithAI();
			DefaultTableModel model = (DefaultTableModel) table.getModel();
			model.setRowCount(0);

			for (Map<String, String> user : users) {
				model.addRow(
						new Object[] { user.get("Username"), user.get("ARN"), user.get("Created"), user.get("AI") });
			}
		} catch (Exception e) {
			JOptionPane.showMessageDialog(this, "Error: " + e.getMessage());
		}
	}

	public static void main(String[] args) {
		SwingUtilities.invokeLater(UnifiedGUI::new);
	}
}
