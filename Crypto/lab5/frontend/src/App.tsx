import Footer from "./components/Footer";
import { Header } from "./components/Header";
import { Tabs } from "./components/Tabs";
import { Form } from "./components/Form";
import { SystemComparisons } from "./components/SystemComparisons";
import { apiConfig } from "./config/apiConfig";

function App() {
  return (
    <div className="bg-bg min-h-screen flex flex-col text-text">
      <Header />

      <main className="flex-1 flex justify-center px-4 py-6">
        <div className="w-full max-w-4xl">
          <Tabs
            tabs={apiConfig}
            render={(tab: any) => {
              if (tab.subtabs) {
                return (
                  <Tabs
                    tabs={tab.subtabs}
                    render={(sub: any) => {
                      if (sub.isDynamic) return <SystemComparisons />;
                      if (!sub.endpoint)
                        return (
                          <div className="text-muted">
                            🚧 В разработке
                          </div>
                        );
                      return <Form config={sub} />;
                    }}
                  />
                );
              }

              return <Form config={tab} />;
            }}
          />
        </div>
      </main>

      <Footer />
    </div>
  );
}

export default App;