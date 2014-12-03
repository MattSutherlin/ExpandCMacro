#
#

import sublime, sublime_plugin, os, ntpath, subprocess, codecs, re

class ExpandCppMacroCommand(sublime_plugin.TextCommand):

	def __init__(self, view):
		self.view = view
		self.regex = re.compile("\s*#define\s+\w+([\s\S]+)")

	def load_settings(self):
		# Variable $project_base_path in settings will be replaced by sublime's project path
		settings = sublime.load_settings("ExpandCMacro.sublime-settings")
		project_path=""
		if sublime.active_window().project_data() is not None:
			project_path = (sublime.active_window().project_data().get("folders")[0].get("path"))

		self.tmp_file_path    = settings.get("tmp_file_path")
		self.default_encoding = settings.get("default_encoding")
		self.include_dirs     = settings.get("include_dirs")
		self.compiler         = settings.get("compiler")
		self.output           = settings.get("output")
		self.other_flags      = settings.get("other_flags")
		for i in range(0, len(self.include_dirs)):
			self.include_dirs[i] = re.sub("(\$project_base_path)", project_path, self.include_dirs[i])

	def run(self, edit):
		self.load_settings()
		view = self.view
		# Find exact Line:Column position of cursor for clang
		pos = view.sel()[0].begin()
		body = view.substr(sublime.Region(0, view.size()))

		line_pos = body[:pos].count('\n')
		file_lines = body.split('\n')

		# Create dummy file which we will send to preprocessor
		tmp_file_header = "#include \""+ntpath.basename(self.view.file_name())+"\"\n"
		line_to_expand = file_lines[line_pos]
		regex_result = re.findall(self.regex, line_to_expand)
		print(regex_result)
		if len(regex_result) > 0:
			line_to_expand = regex_result[0]

		with open(self.tmp_file_path, "w", encoding='UTF-8') as tmp_file:
			tmp_file.write(tmp_file_header + line_to_expand + "\n")
	
		# By default I assumed clang, but gcc should work as well
		clang_bin = self.compiler
		clang_flags = " -E "
		clang_target = self.tmp_file_path
		clang_includes=" -I ."
		for dir in self.include_dirs:
			clang_includes += " -I " + dir

		# Execute clang command, exit 0 to suppress error from check_output()
		clang_cmd = clang_bin + " " + clang_flags + clang_target + clang_includes + " " + self.other_flags
		output = subprocess.check_output(clang_cmd+" | tail -n 2;exit 0", shell=True)
		view.window().create_output_panel(name="test")
		output_text = ''.join(map(chr,output))
		output_lines = output_text.split('\n')

		# Retrieve result and show it to user
		result = output_lines[-2]

		# Create output panel
		self.output_view = view.window().get_output_panel("expand")
		self.output_view.set_read_only(False)

		self.output_view.set_syntax_file(view.settings().get('syntax'))
		region = sublime.Region(0, self.output_view.size())
		self.output_view.erase(edit, region)
		self.output_view.insert(edit, 0, result)

		self.output_view.set_read_only(True)
		view.window().run_command("show_panel", {"panel": "output.expand"})



