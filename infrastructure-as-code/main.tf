

# variable "files" {
#   default = 5
# }

# resource "local_file" "foo" {
#   count    = var.files
#   content  = "# Some content for file ${count.index}"
#   filename = "file${count.index}.txt"
# }

resource "local_file" "foo" {
  for_each = toset(["0", "2", "3", "4"])

  content  = "# Some content for file ${each.key}"
  filename = "file${each.key}.txt"
}