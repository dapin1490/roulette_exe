#include <iostream>
#include <vector>
#include <random> // 균등 난수 참고: https://modoocode.com/304
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
	mt19937 gen = mt19937(random_device{}()); // 난수 생성기

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

	cout << "\n종료하려면 아무 키나 누르기\n";
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

	cout << "\n# 룰렛 입력 시작\n룰렛에 입력할 내용을 엔터로 구분해 작성한 텍스트 파일의 경로를 입력. 파일의 내용이 자동으로 입력됨.\n\n";

	cout << "\n파일 경로 입력: ";
	getline(cin, file_route);

	in = ifstream{ file_route };

	if (in.fail()) {
		cout << "ERROR: 파일 열기 실패\n";
		return;
	}

	while (in.peek() != EOF) {
		getline(in, line);
		candidates.push_back(line);
	}

	in.close();

	cout << "파일 입력 완료\n";

	return;
}

void Roulette::get_console() {
	string line = "";

	cout << "\n# 룰렛 입력 시작\n내용 작성 후 엔터를 누르면 입력되고, 다음 줄에 계속 입력할 수 있음. 0을 입력하거나 빈 줄에 엔터를 누르면 입력 종료.\n";

	while (true) {
		cout << "내용 입력: ";
		getline(cin, line);
		if (line == "0" || line.empty()) {
			cout << "입력 종료\n";
			break;
		}
		candidates.push_back(line);
	}

	return;
}

void Roulette::pick() {
	int winner;

	if (candidates.size() < 1) {
		cout << "ERROR: 룰렛이 비어 있음\n";
		return;
	}

	uniform_int_distribution<int> picker(0, int(candidates.size()) - 1);

	cout << "\n결과 선택 시작\n";

	winner = picker(gen);

	cout << "결과: " << candidates[winner] << "\n";

	return;
}

void Roulette::execute() {
	string buf;
	int input_flag = 1;
	string repick = "y";
	string file_route;

	cout << "=== 룰렛 ===\nmade by dapin1490 on C++\n\n";

	// 룰렛 입력 방식 선택
	cout << "# 룰렛 입력 방식 선택\n";
	cout << "1. 직접 입력: 룰렛에 입력할 내용을 직접 입력. 엔터로 구분하며 '0'을 입력하면 입력 종료.\n";
	cout << "2. 파일로 입력: 룰렛에 입력할 내용이 엔터로 구분되어 작성된 파일의 경로를 입력. 파일의 내용이 자동으로 입력됨.\n";
	cout << "기본값은 직접 입력\n";
	cout << "선택 [1/2]: ";
	getline(cin, buf);
	cout << "\n";

	if (buf != "1" && buf != "2") {
		cout << "입력 방식 기본값으로 진행\n";
		input_flag = 1;
	}
	else {
		input_flag = stoi(buf);
	}

	// 선택한 입력 방식 지정
	set_input_type(input_flag);

	// 입력 실행
	switch (input_type) {
	case CONSOLE: get_console(); break;
	case FILE: get_file(); break;
	}

	// 룰렛 실행
	cout << "\n# 룰렛 실행\n";
	while (repick == "y" || repick == "Y") {
		pick();

		if (candidates.size() < 1)
			break;

		cout << "\n다시 뽑기(기본값 y) [Y/n]: ";
		getline(cin, buf);

		if (!buf.empty()) {
			repick = buf;
		}
	}

	cout << "\n# 룰렛 종료\n";

	return;
}