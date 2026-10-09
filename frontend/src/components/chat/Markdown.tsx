import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { oneDark } from "react-syntax-highlighter/dist/esm/styles/prism";

export function Markdown({ children }: { children: string }) {
    return (
        <ReactMarkdown
            remarkPlugins={[remarkGfm]}
            components={{
                code(props) {
                    const { children, className, ...rest } = props;

                    const match = /language-(\w+)/.exec(
                        className || ""
                    );

                    if (!match) {
                        return (
                            <code
                                className="rounded bg-muted px-1.5 py-0.5 text-sm font-mono"
                                {...rest}
                            >
                                {children}
                            </code>
                        );
                    }

                    return (
                        <SyntaxHighlighter
                            language={match[1]}
                            style={oneDark}
                            PreTag="div"
                        >
                            {String(children).replace(/\n$/, "")}
                        </SyntaxHighlighter>
                    );
                },
            }}
        >
            {children}
        </ReactMarkdown>
    );
}