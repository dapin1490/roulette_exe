#include <iostream>
#include <vector>
#include <random> // �յ� ���� ����: https://modoocode.com/304
#include <string>
#include <fstream>
#include <conio.h>
using namespace std;

class Roulette {
public:
	enum input_t { CONSOLE, FILE };
private:
	vector<string> candidates;
	input_t input_type;
	mt19937 gen = mt19937(random_device{}()); // ���� ������

private:
	void set_input_type(int code);
	void get_file();
	void get_console();
	void pick();
public:
	Roulette() {
		this->input_type = CONSOLE;
	}

	void execute();
};

int main()
{
	Roulette roulette = Roulette();

	roulette.execute();

	cout << "\n�����Ϸ��� �ƹ� Ű�� ������\n";
	char ch = _getch();
	return 0;
}

void Roulette::set_input_type(int code) {
	switch (code) {
	case 1: input_type = CONSOLE; break;
	case 2: input_type = FILE; break;
	}
	return;
}

void Roulette::get_file() {
	string file_route;
	string line;
	ifstream in;

	cout << "\n# �귿 �Է� ����\n�귿�� �Է��� ������ ���ͷ� ������ �ۼ��� �ؽ�Ʈ ������ ��θ� �Է�. ������ ������ �ڵ����� �Էµ�.\n\n";

	cout << "\n���� ��� �Է�: ";
	getline(cin, file_route);

	in = ifstream{ file_route };

	if (in.fail()) {
		cout << "ERROR: ���� ���� ����\n";
		return;
	}

	while (in.peek() != EOF) {
		getline(in, line);
		candidates.push_back(line);
	}

	in.close();

	cout << "���� �Է� �Ϸ�\n";

	return;
}

void Roulette::get_console() {
	string line = "";

	cout << "\n# �귿 �Է� ����\n���� �ۼ� �� ���͸� ������ �Էµǰ�, ���� �ٿ� ��� �Է��� �� ����. 0�� �Է��ϰų� �� �ٿ� ���͸� ������ �Է� ����.\n";

	while (true) {
		cout << "���� �Է�: ";
		getline(cin, line);
		if (line == "0" || line.empty()) {
			cout << "�Է� ����\n";
			break;
		}
		candidates.push_back(line);
	}

	return;
}

void Roulette::pick() {
	int winner;

	if (candidates.size() < 1) {
		cout << "ERROR: �귿�� ��� ����\n";
		return;
	}

	uniform_int_distribution<int> picker(0, int(candidates.size()) - 1);

	cout << "\n��� ���� ����\n";

	winner = picker(gen);

	cout << "���: " << candidates[winner] << "\n";

	return;
}

void Roulette::execute() {
	string buf;
	int input_flag = 1;
	string repick = "y";
	string file_route;

	cout << "=== �귿 ===\nmade by dapin1490 on C++\n\n";

	// �귿 �Է� ��� ����
	cout << "# �귿 �Է� ��� ����\n";
	cout << "1. ���� �Է�: �귿�� �Է��� ������ ���� �Է�. ���ͷ� �����ϸ� '0'�� �Է��ϸ� �Է� ����.\n";
	cout << "2. ���Ϸ� �Է�: �귿�� �Է��� ������ ���ͷ� ���еǾ� �ۼ��� ������ ��θ� �Է�. ������ ������ �ڵ����� �Էµ�.\n";
	cout << "�⺻���� ���� �Է�\n";
	cout << "���� [1/2]: ";
	getline(cin, buf);
	cout << "\n";

	if (buf != "1" && buf != "2") {
		cout << "�Է� ��� �⺻������ ����\n";
		input_flag = 1;
	}
	else {
		input_flag = stoi(buf);
	}

	// ������ �Է� ��� ����
	set_input_type(input_flag);

	// �Է� ����
	switch (input_type) {
	case CONSOLE: get_console(); break;
	case FILE: get_file(); break;
	}

	// �귿 ����
	cout << "\n# �귿 ����\n";
	while (repick == "y" || repick == "Y") {
		pick();

		if (candidates.size() < 1)
			break;

		cout << "\n�ٽ� �̱�(�⺻�� y) [Y/n]: ";
		getline(cin, buf);

		if (!buf.empty()) {
			repick = buf;
		}
	}

	cout << "\n# �귿 ����\n";

	return;
}