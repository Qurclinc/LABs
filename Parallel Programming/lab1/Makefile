# Compiler & flags
CXX:=g++
CXXFLAGS:=-fopenmp -fpermissive

# Directories
SRC_DIR:=src
BUILD_DIR:=build
TARGET:=main

# Files
SRCS := $(wildcard $(SRC_DIR)/*.cpp)
OBJS := $(patsubst $(SRC_DIR)/%.cpp, $(BUILD_DIR)/%.o, $(SRCS))

# Default
all: $(TARGET)

# Link
$(TARGET): $(OBJS)
	$(CXX) $(CXXFLAGS) $^ -o $@

# Compile
$(BUILD_DIR)/%.o: $(SRC_DIR)/%.cpp
	@mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) -c $< -o $@

clean:
	rm -rf $(BUILD_DIR) $(TARGET)

.PHONY: all clean