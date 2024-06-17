package org.un.undf.model;

public class Aluno {
	private int id;
	private String nome;
	private String cpf;
	private String senha;
	private String curso;

	public Aluno(int id, String nome, String cpf, String senha, String curso) {
		this.id = id;
		this.nome = nome;
		this.cpf = cpf;
		this.senha = senha;
		this.curso = curso;
	}

	public Aluno(String nome, String cpf, String curso) {
		this.nome = nome;
		this.cpf = cpf;
		this.curso = curso;
	}

	public Aluno(String nome, String cpf, String senha, String curso) {
		this.nome = nome;
		this.cpf = cpf;
		this.senha = senha;
		this.curso = curso;
	}

	public int getId() {
		return id;
	}

	public void setId(int id) {
		this.id = id;
	}

	public String getNome() {
		return nome;
	}

	public void setNome(String nome) {
		this.nome = nome;
	}

	public String getCpf() {
		return cpf;
	}

	public void setCpf(String cpf) {
		this.cpf = cpf;
	}

	public String getSenha() {
		return senha;
	}

	public void setSenha(String senha) {
		this.senha = senha;
	}

	public String getCurso() {
		return curso;
	}

	public void setCurso(String email) {
		this.curso = email;
	}

}
